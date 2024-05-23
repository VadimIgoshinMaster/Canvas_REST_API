import requests
import json
from datetime import datetime, timedelta

# Your Canvas API token
API_TOKEN = '13016~YcQy4fQaxVX6ssHbe1uDBIDEK8V83W0yPPVbwe1rgTV2OX8PswwuAzf3bra2zYV0'
# Canvas API base URL
API_BASE_URL = 'https://wust.instructure.com/api/v1'
# List of course IDs you want to update
COURSE_IDS = [4495, 4485, 4486]

# Number of days to shift
DAYS_SHIFT = 98

# Function to shift dates
def shift_date(date_str, days_shift):
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        new_date = date + timedelta(days=days_shift)
        return new_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return date_str

# Function to get all assignments in a course
def get_assignments(course_id):
    url = f"{API_BASE_URL}/courses/{course_id}/assignments"
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Function to update an assignment
def update_assignment(course_id, assignment_id, due_at, unlock_at, lock_at):
    url = f"{API_BASE_URL}/courses/{course_id}/assignments/{assignment_id}"
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'assignment': {
            'due_at': due_at,
            'unlock_at': unlock_at,
            'lock_at': lock_at
        }
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()

# Loop through each course and update assignments
for course_id in COURSE_IDS:
    assignments = get_assignments(course_id)
    for assignment in assignments:
        new_due_at = shift_date(assignment['due_at'], DAYS_SHIFT)
        new_unlock_at = shift_date(assignment['unlock_at'], DAYS_SHIFT)
        new_lock_at = shift_date(assignment['lock_at'], DAYS_SHIFT)
        update_assignment(course_id, assignment['id'], new_due_at, new_unlock_at, new_lock_at)
        print(f"Updated assignment {assignment['name']} in course {course_id}")

print("All assignments updated successfully.")