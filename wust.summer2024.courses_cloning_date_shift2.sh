#!/bin/bash

# Configuration
API_URL="https://wust.instructure.com/api/v1"
ACCESS_TOKEN="13016~YcQy4fQaxVX6ssHbe1uDBIDEK8V83W0yPPVbwe1rgTV2OX8PswwuAzf3bra2zYV0"
CSV_FILE="courses_to_clone.csv"

# Function to copy course content with date adjustment
copy_course_content() {
    local source_course_id=$1
    local destination_course_id=$2
    local original_start_date=$3
    local original_end_date=$4
    local new_start_date=$5
    local new_end_date=$6

    # Date shift options
    date_shift_options=$(jq -n --arg osd "$original_start_date" --arg oed "$original_end_date" --arg nsd "$new_start_date" --arg ned "$new_end_date" '{
        "old_start_date": $osd,
        "old_end_date": $oed,
        "new_start_date": $nsd,
        "new_end_date": $ned
    }')

   # Construct the JSON payload
    json_payload=$(jq -n --arg sc "$source_course_id" --arg mt "course_copy_importer" --argjson dso "$date_shift_options" '{
        "source_course": $sc,
        "migration_type": $mt,
        "date_shift_options": $dso
    }')

    # Initiate course copy with date adjustment
    response=$(curl -s -X POST \
        "$API_URL/courses/$destination_course_id/course_copy" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        --data "$json_payload")

    # Extract migration ID
    migration_id=$(echo $response | jq -r '.id')
    if [ "$migration_id" = "null" ]; then
        echo "Failed to initiate content copy from course $source_course_id to $destination_course_id"
        echo "Response: $response"
        return
    fi

    echo "Successfully initiated content copy from course $source_course_id to $destination_course_id"
    echo "Migration ID: $migration_id"

    # Check migration status
    check_migration_status $destination_course_id $migration_id
}

# Function to check the migration status
check_migration_status() {
    local course_id=$1
    local migration_id=$2

    while true; do
        response=$(curl -s -X GET \
            "$API_URL/courses/$course_id/content_migrations/$migration_id" \
            -H "Authorization: Bearer $ACCESS_TOKEN")

        migration_status=$(echo $response | jq -r '.workflow_state')
        echo "Content migration status for course $course_id: $migration_status"

        if [ "$migration_status" = "completed" ]; then
            echo "Content copy completed for course $course_id"
            break
        elif [ "$migration_status" = "failed" ]; then
            echo "Content copy failed for course $course_id"
            break
        fi

        sleep 10  # Wait for 10 seconds before checking again
    done
}

# Read the CSV file and clone courses with date adjustment
while IFS=, read -r source_course_id destination_course_id original_start_date original_end_date new_start_date new_end_date; do
    # Skip header row
    if [ "$source_course_id" = "source_course_id" ]; then
        continue
    fi

    copy_course_content $source_course_id $destination_course_id $original_start_date $original_end_date $new_start_date $new_end_date
done < $CSV_FILE

echo "Course cloning process completed."