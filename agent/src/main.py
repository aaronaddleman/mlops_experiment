from fastapi import FastAPI, HTTPException, Depends
from prometheus_client import make_asgi_app, Counter, Histogram, Gauge
import time
from datetime import datetime, time as dt_time
from typing import List, Optional
import numpy as np
from sqlalchemy.orm import Session
from .models.database import User, Habit, HabitCompletion, get_db
from .models.habit import Habit as HabitModel, HabitCompletion as HabitCompletionModel, UserProfile

app = FastAPI(title="Habit Wizard Agent")

# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Define metrics
request_counter = Counter('agent_requests_total', 'Total number of requests')
request_latency = Histogram('agent_request_latency_seconds', 'Request latency in seconds')
active_habits = Gauge('active_habits_total', 'Number of active habits')
habit_completion_rate = Gauge('habit_completion_rate', 'Average habit completion rate')

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
async def create_user(user: UserProfile, db: Session = Depends(get_db)):
    db_user = User(
        id=user.id,
        name=user.name,
        preferred_notification_time=user.preferred_notification_time,
        timezone=user.timezone,
        created_at=user.created_at
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user

@app.get("/users/{user_id}", response_model=UserProfile)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserProfile(
        id=db_user.id,
        name=db_user.name,
        email=db_user.email
    )

@app.post("/habits/", response_model=HabitModel)
async def create_habit(habit: HabitModel, user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_habit = Habit(
        id=habit.id,
        user_id=user_id,
        name=habit.name,
        description=habit.description,
        frequency=habit.frequency,
        target_time=habit.target_time,
        difficulty=habit.difficulty,
        category=habit.category
    )
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    
    active_habits.inc()
    return habit

@app.get("/habits/{habit_id}", response_model=HabitModel)
async def get_habit(habit_id: str, db: Session = Depends(get_db)):
    db_habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    return HabitModel(
        id=db_habit.id,
        name=db_habit.name,
        description=db_habit.description,
        frequency=db_habit.frequency,
        target_time=db_habit.target_time,
        created_at=db_habit.created_at,
        difficulty=db_habit.difficulty,
        category=db_habit.category
    )

@app.post("/completions/", response_model=HabitCompletionModel)
async def record_completion(completion: HabitCompletionModel, db: Session = Depends(get_db)):
    db_habit = db.query(Habit).filter(Habit.id == completion.habit_id).first()
    if not db_habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    db_completion = HabitCompletion(
        habit_id=completion.habit_id,
        completed_at=completion.completed_at,
        notes=completion.notes,
        mood=completion.mood,
        difficulty=completion.difficulty
    )
    db.add(db_completion)
    
    # Update habit stats
    db_habit.last_completed = completion.completed_at
    db_habit.streak += 1
    
    # Update success rate
    total_completions = db.query(HabitCompletion).filter(
        HabitCompletion.habit_id == completion.habit_id
    ).count()
    db_habit.success_rate = total_completions / 30  # Assuming 30-day window
    
    db.commit()
    db.refresh(db_completion)
    
    # Update metrics
    habit_completion_rate.set(db_habit.success_rate)
    
    return completion

@app.get("/analytics/{user_id}")
async def get_user_analytics(user_id: str, db: Session = Depends(get_db)):
    # Get all habits for the user
    user_habits = db.query(Habit).filter(Habit.user_id == user_id).all()
    total_habits = len(user_habits)
    
    if total_habits == 0:
        return {
            "total_habits": 0,
            "average_success_rate": 0.0,
            "total_streaks": 0,
            "habits_by_category": {}
        }

    # Calculate success rate
    total_completions = sum(
        db.query(HabitCompletion).filter(
            HabitCompletion.habit_id.in_([h.id for h in user_habits])
        ).count()
    )
    success_rate = (total_completions / (total_habits * 30)) * 100 if total_habits > 0 else 0.0
    
    # Count streaks
    total_streaks = sum(h.streak for h in user_habits)
    
    # Group habits by category
    habits_by_category = {}
    for habit in user_habits:
        if habit.category not in habits_by_category:
            habits_by_category[habit.category] = 0
        habits_by_category[habit.category] += 1
    
    return {
        "total_habits": total_habits,
        "average_success_rate": float(success_rate),
        "total_streaks": total_streaks,
        "habits_by_category": habits_by_category
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    users_count = db.query(User).count()
    habits_count = db.query(Habit).count()
    completions_count = db.query(HabitCompletion).count()
    
    return {
        "status": "healthy",
        "users_count": users_count,
        "habits_count": habits_count,
        "completions_count": completions_count
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 