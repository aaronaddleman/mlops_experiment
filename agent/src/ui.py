from flask import Flask, render_template, request, jsonify
import threading
import time
import requests
import random
from datetime import datetime, timedelta
from collections import deque

app = Flask(__name__)

# Preset tasks
PRESET_TASKS = [
    {"id": f"task_{i}", "name": f"Task {i}", "description": f"Description for task {i}", 
     "category": random.choice(["health", "work", "personal", "learning"]),
     "difficulty": random.randint(1, 5)} 
    for i in range(1, 21)
]

# Global state
active_tasks = set()
generation_interval = 10  # seconds
is_running = False
agent_thread = None
last_event_time = None
# Store last 100 log messages
log_messages = deque(maxlen=100)

def log_message(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_messages.append(f"[{timestamp}] {message}")

def generate_habit():
    global last_event_time
    while is_running:
        if active_tasks:
            # Select a random active task
            task_id = random.choice(list(active_tasks))
            task = next(t for t in PRESET_TASKS if t["id"] == task_id)
            
            # Create habit
            habit_data = {
                "id": f"habit_{datetime.now().timestamp()}",
                "name": task["name"],
                "description": task["description"],
                "frequency": "daily",
                "target_time": "09:00:00",
                "created_at": datetime.now().isoformat(),
                "difficulty": task["difficulty"],
                "category": task["category"]
            }
            
            log_message(f"Creating habit: {task['name']}")
            
            # Create habit
            habit_response = requests.post(
                "http://agent:8000/habits/",
                json=habit_data
            )
            
            if habit_response.status_code == 200:
                habit_id = habit_response.json()["id"]
                
                # Create completion
                completion_data = {
                    "habit_id": habit_id,
                    "completed_at": datetime.now().isoformat(),
                    "notes": f"Automated completion for {task['name']}",
                    "mood": random.randint(1, 5),
                    "difficulty": random.randint(1, 5)
                }
                
                log_message(f"Completing habit: {task['name']} (Mood: {completion_data['mood']}, Difficulty: {completion_data['difficulty']})")
                
                completion_response = requests.post(
                    "http://agent:8000/completions/",
                    json=completion_data
                )
                
                if completion_response.status_code == 200:
                    log_message(f"Successfully completed habit: {task['name']}")
                else:
                    log_message(f"Failed to complete habit: {task['name']}")
            
            last_event_time = datetime.now()
        time.sleep(generation_interval)

@app.route('/')
def index():
    return render_template('index.html', tasks=PRESET_TASKS, 
                         active_tasks=active_tasks, 
                         interval=generation_interval,
                         is_running=is_running)

@app.route('/toggle_task', methods=['POST'])
def toggle_task():
    task_id = request.json.get('task_id')
    if task_id in active_tasks:
        active_tasks.remove(task_id)
        log_message(f"Deactivated task: {task_id}")
    else:
        active_tasks.add(task_id)
        log_message(f"Activated task: {task_id}")
    return jsonify({"status": "success"})

@app.route('/set_interval', methods=['POST'])
def set_interval():
    global generation_interval
    interval = request.json.get('interval')
    if interval and isinstance(interval, (int, float)) and interval > 0:
        generation_interval = interval
        log_message(f"Updated generation interval to {interval} seconds")
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Invalid interval"}), 400

@app.route('/toggle_agent', methods=['POST'])
def toggle_agent():
    global is_running, agent_thread, last_event_time
    is_running = not is_running
    
    if is_running and not agent_thread:
        log_message("Starting habit generation")
        last_event_time = datetime.now()  # Initialize last_event_time when starting
        agent_thread = threading.Thread(target=generate_habit)
        agent_thread.daemon = True
        agent_thread.start()
    elif not is_running:
        log_message("Stopping habit generation")
    
    return jsonify({"status": "success", "is_running": is_running})

@app.route('/logs')
def get_logs():
    return jsonify({"logs": list(log_messages)})

@app.route('/next_event_time')
def get_next_event_time():
    if not is_running or not last_event_time:
        return jsonify({"next_event_time": None})
    
    next_time = last_event_time + timedelta(seconds=generation_interval)
    return jsonify({"next_event_time": next_time.isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 