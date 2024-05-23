###### SIS Batch Upload ############
#1. Update users.csv with relevant info from Populi, new instructors should be added.
#2. Update courses3.csv with relevant info from Populi, all the course for the new term should be added.
#3. Update the enrollments3.csv with relevant info from Populi. Retrive all instructors PopuliID = user_id from https://wust.populiweb.com/router/academics/academicterms/303045/faculty.
#4. Run users.csv fil in Canvas SIS to create new instructors' accounts.
#5. Run courses3.csv in Canvas SIS to create new courses shells

###### API Batch Upload ##########
#6. Update courses_to_clone.csv with relevat sourses IDs
#7. Run the courses.cloning_date_shift2.sh to clone all the content from previous term courses and Templates
