from fastapi import FastAPI, HTTPException
from prometheus_client import make_asgi_app, Counter, Histogram, Gauge
import time
from datetime import datetime, time as dt_time
from typing import List, Optional
import numpy as np
from .models.habit import Habit, HabitCompletion, UserProfile

app = FastAPI(title="Habit Wizard Agent")

# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Define metrics
request_counter = Counter('agent_requests_total', 'Total number of requests')
request_latency = Histogram('agent_request_latency_seconds', 'Request latency in seconds')
active_habits = Gauge('active_habits_total', 'Number of active habits')
habit_completion_rate = Gauge('habit_completion_rate', 'Average habit completion rate')

# In-memory storage (replace with database in production)
users = {}
habits = {}
completions = []

@app.get("/")
async def root():
    with request_latency.time():
        request_counter.inc()
        return {
            "message": "Habit Wizard Agent is running",
            "version": "1.0.0",
            "features": [
                "Habit tracking",
                "Personalized motivation",
                "Progress analytics",
                "Streak management"
            ]
        }

@app.post("/users/", response_model=UserProfile)
async def create_user(user: UserProfile):
    users[user.id] = user
    return user

@app.get("/users/{user_id}", response_model=UserProfile)
async def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.post("/habits/", response_model=Habit)
async def create_habit(habit: Habit, user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    habits[habit.id] = habit
    users[user_id].habits.append(habit)
    active_habits.inc()
    return habit

@app.get("/habits/{habit_id}", response_model=Habit)
async def get_habit(habit_id: str):
    if habit_id not in habits:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habits[habit_id]

@app.post("/completions/", response_model=HabitCompletion)
async def record_completion(completion: HabitCompletion):
    if completion.habit_id not in habits:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    completions.append(completion)
    habit = habits[completion.habit_id]
    habit.last_completed = completion.completed_at
    habit.streak += 1
    
    # Update success rate
    total_completions = len([c for c in completions if c.habit_id == habit.id])
    habit.success_rate = total_completions / 30  # Assuming 30-day window
    
    # Update metrics
    habit_completion_rate.set(habit.success_rate)
    
    return completion

@app.get("/analytics/{user_id}")
async def get_user_analytics(user_id: str):
    # Get all habits for the user
    habits = [h for h in habits.values() if h.user_id == user_id]
    total_habits = len(habits)
    
    if total_habits == 0:
        return {
            "total_habits": 0,
            "average_success_rate": 0,
            "total_streaks": 0,
            "habits_by_category": {}
        }

    # Calculate success rate
    total_completions = len([c for c in completions if c.habit_id in [h.id for h in habits]])
    success_rate = (total_completions / (total_habits * 30)) * 100 if total_habits > 0 else 0
    
    # Count streaks (simplified)
    total_streaks = total_completions  # For now, each completion counts as a streak
    
    # Group habits by category
    habits_by_category = {}
    for habit in habits:
        if habit.category not in habits_by_category:
            habits_by_category[habit.category] = 0
        habits_by_category[habit.category] += 1
    
    return {
        "total_habits": total_habits,
        "average_success_rate": float(success_rate),  # Ensure it's a float
        "total_streaks": total_streaks,
        "habits_by_category": habits_by_category
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "users_count": len(users),
        "habits_count": len(habits),
        "completions_count": len(completions)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 