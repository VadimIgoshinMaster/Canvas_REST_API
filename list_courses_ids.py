import requests
import csv

# Replace with your actual Canvas API URL and API token
canvas_base_url = 'https://wust.instructure.com'  # Ensure this is correct
api_token = '13016~YcQy4fQaxVX6ssHbe1uDBIDEK8V83W0yPPVbwe1rgTV2OX8PswwuAzf3bra2zYV0'  # Ensure this is correct and has necessary permissions
account_id = '1'  # Ensure this is the correct account ID
term_id = '235'  # Ensure this is the correct term ID

# Set up the API request
headers = {
    'Authorization': f'Bearer {api_token}'
}
url = f'{canvas_base_url}/api/v1/accounts/{account_id}/courses'

# Add the term parameter to the request
params = {
    'enrollment_term_id': term_id,
    'per_page': 100  # Request more courses per page (max is typically 100)
}

# Function to get all pages of results
def get_all_courses(url, headers, params):
    courses = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break
        courses.extend(response.json())
        # Get the next page URL from the 'Link' header
        link_header = response.headers.get('Link', '')
        next_url = None
        for link in link_header.split(','):
            if 'rel="next"' in link:
                next_url = link[link.find('<') + 1:link.find('>')]
        url = next_url
        params = {}  # Clear params after the first request
    return courses

# Get all courses
all_courses = get_all_courses(url, headers, params)

# Define the CSV file name
csv_file_name = 'all_courses_term.csv'

# Write to CSV
with open(csv_file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Course ID', 'Course Name', 'Course Code', 'Start Date', 'End Date', 'Workflow State'])
    # Write the course data
    for course in all_courses:
        writer.writerow([
            course['id'],
            course['name'],
            course.get('course_code', ''),
            course.get('start_at', ''),
            course.get('end_at', ''),
            course['workflow_state']
        ])

print(f"All courses for term {term_id} have been written to {csv_file_name}")