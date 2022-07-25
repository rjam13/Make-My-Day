from questions.models import Response, Question, Answer


def calculate_student_section_score(student, section):
    questions = Question.objects.filter(section=section)
    all_responses = Response.objects.filter(student=student, question__in=questions)
    num_correct = 0
    num_total_responses = len(all_responses)
    
    for response in all_responses:
        if response.answer.is_correct:
            num_correct = num_correct + 1


    return round((num_correct / num_total_responses) * 100, 2)