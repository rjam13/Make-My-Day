from main.models import Course

def student_access_only(request):
    pass

def instructor_access_only(request):
    pass

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
    if Course.objects.get(course_id=course_id).instructor.instructor_id == instructor_id:
        return True
    else:
        return False

