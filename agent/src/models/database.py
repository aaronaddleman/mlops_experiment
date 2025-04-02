from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Create database directory if it doesn't exist
os.makedirs('/app/data', exist_ok=True)

# Create SQLite engine
engine = create_engine('sqlite:////app/data/habits.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    preferred_notification_time = Column(Time)
    timezone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    habits = relationship("Habit", back_populates="user")

class Habit(Base):
    __tablename__ = "habits"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    description = Column(String)
    frequency = Column(String)
    target_time = Column(Time)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_completed = Column(DateTime, nullable=True)
    streak = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    difficulty = Column(Integer)
    category = Column(String)
    is_active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="habits")
    completions = relationship("HabitCompletion", back_populates="habit")

class HabitCompletion(Base):
    __tablename__ = "habit_completions"
    
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(String, ForeignKey("habits.id"))
    completed_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    mood = Column(Integer)
    difficulty = Column(Integer)
    
    habit = relationship("Habit", back_populates="completions")

# Create all tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 