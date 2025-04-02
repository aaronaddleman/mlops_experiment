from datetime import datetime, time
from src.models.habit import Habit, HabitCompletion, UserProfile

def test_habit_creation():
    habit = Habit(
        id="test1",
        name="Morning Exercise",
        description="30 minutes of exercise",
        frequency="daily",
        target_time=time(7, 0),
        created_at=datetime.now(),
        difficulty=3,
        category="health"
    )
    
    assert habit.id == "test1"
    assert habit.name == "Morning Exercise"
    assert habit.frequency == "daily"
    assert habit.difficulty == 3
    assert habit.category == "health"
    assert habit.streak == 0
    assert habit.success_rate == 0.0

def test_habit_completion_creation():
    completion = HabitCompletion(
        habit_id="test1",
        completed_at=datetime.now(),
        notes="Felt great today!",
        mood=5,
        difficulty=2
    )
    
    assert completion.habit_id == "test1"
    assert completion.notes == "Felt great today!"
    assert completion.mood == 5
    assert completion.difficulty == 2

def test_user_profile_creation():
    user = UserProfile(
        id="user1",
        name="Test User",
        habits=[],
        preferred_notification_time=time(9, 0),
        timezone="UTC",
        created_at=datetime.now()
    )
    
    assert user.id == "user1"
    assert user.name == "Test User"
    assert len(user.habits) == 0
    assert user.preferred_notification_time == time(9, 0)
    assert user.timezone == "UTC" 