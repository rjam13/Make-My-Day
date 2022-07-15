from main.models import UserProfile, Student, Instructor

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def retrieveStudent(request):
    try:
        user = request.user
        userProfile = UserProfile.objects.filter(user=user)[0]
        student = Student.objects.filter(user_profile = userProfile)[0]
        return student
    except:
        return None

def retrieveInstructor(request):
    try:
        user = request.user
        userProfile = UserProfile.objects.filter(user=user)[0]
        instructor = Instructor.objects.filter(user_profile = userProfile)[0]
        return instructor
    except:
        return None


