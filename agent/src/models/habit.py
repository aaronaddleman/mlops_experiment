from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, time

class Habit(BaseModel):
    id: str
    name: str
    description: str
    frequency: str  # daily, weekly, etc.
    target_time: Optional[time] = None
    created_at: datetime
    last_completed: Optional[datetime] = None
    streak: int = 0
    success_rate: float = 0.0
    difficulty: int  # 1-5 scale
    category: str  # health, learning, productivity, etc.

class HabitCompletion(BaseModel):
    habit_id: str
    completed_at: datetime
    notes: Optional[str] = None
    mood: Optional[int] = None  # 1-5 scale
    difficulty: Optional[int] = None  # 1-5 scale

class UserProfile(BaseModel):
    id: str
    name: str
    habits: List[Habit]
    preferred_notification_time: time
    timezone: str
    created_at: datetime 