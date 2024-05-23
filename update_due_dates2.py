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

# Function to get all assignments in a course with pagination handling
def get_assignments(course_id):
    url = f"{API_BASE_URL}/courses/{course_id}/assignments"
    headers = {'Authorization': f'Bearer {API_TOKEN}'}
    assignments = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        assignments.extend(response.json())
        # Handle pagination
        if 'next' in response.links:
            url = response.links['next']['url']
        else:
            url = None
    return assignments

# Function to update an assignment
def update_assignment(course_id, assignment):
    url = f"{API_BASE_URL}/courses/{course_id}/assignments/{assignment['id']}"
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'assignment': {
            'due_at': assignment['due_at'],
            'unlock_at': assignment['unlock_at'],
            'lock_at': assignment['lock_at'],
            'assignment_overrides': assignment.get('assignment_overrides', [])
        }
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()

# Loop through each course and update assignments
for course_id in COURSE_IDS:
    assignments = get_assignments(course_id)
    for assignment in assignments:
        assignment['due_at'] = shift_date(assignment['due_at'], DAYS_SHIFT)
        assignment['unlock_at'] = shift_date(assignment['unlock_at'], DAYS_SHIFT)
        assignment['lock_at'] = shift_date(assignment['lock_at'], DAYS_SHIFT)
        updated_assignment = update_assignment(course_id, assignment)
        print(f"Updated assignment {assignment['name']} in course {course_id}")

print("All assignments updated successfully.")