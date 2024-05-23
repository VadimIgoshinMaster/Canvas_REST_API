# chmod +x wust.summer2024.courses_cloning.sh
# ./wust.summer2024.courses_cloning.sh


#IT501-1
curl -X POST \
'https://wust.instructure.com/api/v1/courses/4487/course_copy' \
-H 'Authorization: Bearer 13016~YcQy4fQaxVX6ssHbe1uDBIDEK8V83W0yPPVbwe1rgTV2OX8PswwuAzf3bra2zYV0' \
-H 'Content-Type: application/json' \
--data-raw '{
  "source_course": "3949",
  "migration_type": "course_copy_importer"
}'

#IT501-2
curl -X POST \
'https://wust.instructure.com/api/v1/courses/4484/course_copy' \
-H 'Authorization: Bearer 13016~YcQy4fQaxVX6ssHbe1uDBIDEK8V83W0yPPVbwe1rgTV2OX8PswwuAzf3bra2zYV0' \
-H 'Content-Type: application/json' \
--data-raw '{
  "source_course": "3950",
  "migration_type": "course_copy_importer"
}'

#IT501-3
curl -X POST \
'https://wust.instructure.com/api/v1/courses/4485/course_copy' \
-H 'Authorization: Bearer 13016~YcQy4fQaxVX6ssHbe1uDBIDEK8V83W0yPPVbwe1rgTV2OX8PswwuAzf3bra2zYV0' \
-H 'Content-Type: application/json' \
--data-raw '{
  "source_course": "3951",
  "migration_type": "course_copy_importer"
}'

#IT501-4
curl -X POST \
'https://wust.instructure.com/api/v1/courses/4486/course_copy' \
-H 'Authorization: Bearer 13016~YcQy4fQaxVX6ssHbe1uDBIDEK8V83W0yPPVbwe1rgTV2OX8PswwuAzf3bra2zYV0' \
-H 'Content-Type: application/json' \
--data-raw '{
  "source_course": "3952",
  "migration_type": "course_copy_importer"
}'