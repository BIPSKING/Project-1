from plyer import notification
import time
import json

def send_notification(task):
    notification.notify(
        title='Task Reminder',
        message=f'Task: {task["task"]}\nTime: {task["time"]}',
        app_name='ReMindApp',
        timeout=10
    )

while True:
    with open('task.json', 'r') as f:
        tasks = json.load(f)
        current_time = time.strftime('%H:%M')
        current_date = time.strftime('%A %d %B %Y')
        for task in tasks:
            if task['time'] == current_time and task['date'] == current_date:
                send_notification(task)
    time.sleep(60)
