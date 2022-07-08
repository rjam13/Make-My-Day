from questions.models import Question_Bank
from main.models import Course, Instructor

def isInstructor(request):
    if request.user.userprofile.instructor_id == "":
        return False
    else:
        return True

def isStudent(request):
    if request.user.userprofile.student_id == "":
        return False
    else:
        return True

def isInstructorOfCourse(request, course_id):
    instructor_id = request.user.userprofile.instructor_id
    if Course.objects.get(course_id=course_id).instructors.filter(instructor_id=instructor_id).exists():
        return True
    else:
        return False

