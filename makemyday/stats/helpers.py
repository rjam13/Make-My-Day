from questions.models import Response, Question, Answer

def is_response_correct(response):
    if Answer.objects.filter(is_correct=True, question=response.question).exists():
        return True
    return False

def calculate_student_section_score(student, section):
    questions = Question.objects.filter(section=section)
    all_responses = Response.objects.filter(student=student, question__in=questions)
    num_correct = 0
    total_responses = len(all_responses)
    
    for response in all_responses:
        if is_response_correct(response):
            num_correct = num_correct + 1


    return (num_correct / total_responses) * 100