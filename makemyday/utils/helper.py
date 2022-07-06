from main.models import UserProfile, Student, Instructor

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def retrieveStudent(request):
    user = request.user
    userProfile = UserProfile.objects.filter(user=user)[0]
    return Student.objects.filter(user_profile = userProfile)[0]

def retrieveInstructor(request):
    user = request.user
    userProfile = UserProfile.objects.filter(user=user)[0]
    return Instructor.objects.filter(user_profile = userProfile)[0]


