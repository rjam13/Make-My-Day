from questions.models import Question_Bank

def isInstructor(request):
    if request.user.userprofile.instructor_id == "":
        return False
    else:
        return True
