from django.shortcuts import render
from main.models import Student, UserProfile
from .models import Question_Bank, Question, Answer, Activated_Question_Bank
from django.views.generic import ListView
from django.http import JsonResponse

# Create your views here.

class QuestionBankListView(ListView):
    model = Question_Bank # sets object_list in main_qb.html
    template_name = 'question_banks/main_qb.html'

def question_bank_view(request, id):
    question_bank = Question_Bank.objects.get(question_bank_id=id)
    return render(request, 'question_banks/qb.html', {'qb': question_bank})

# called injunction with question_bank_view
def qb_data_view(request, id):
    question_bank = Question_Bank.objects.get(question_bank_id=id)
    questions = []
    for q in question_bank.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.ans)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time_Limit': question_bank.time_Limit,
    })

# called when submitting quiz from website
def save_qb_view(request, id):
    # print(request.POST)
    if is_ajax(request):
        questions = []
        data = request.POST
        data_ = dict(data.lists()) # contains all the answers provided where keys = questions, values = answers
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(ques=k)
            questions.append(question)
        print(questions)

        # retrieves the student that answered the qb
        user = request.user
        userProf = UserProfile.objects.filter(user=user)[0]
        student = Student.objects.filter(user_profile = userProf)[0]
        
        qb = Question_Bank.objects.get(question_bank_id=id)

        # calculating score and collecting each answer provided, paired with the correct answer, into results
        score = 0
        multiplier = 100 / len(questions)
        results = []
        correct_answer = None

        for q in questions:
            # find the selected answer for the corresponding question
            a_selected = request.POST.get(q.ques) 

            # if questions is answered
            if a_selected != "":
                # goes through all the answers of the question, finds the correct one and compares to selected answer
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.ans:
                        if a.isCorrect:
                            score += 1
                            correct_answer = a.ans
                    else:
                        if a.isCorrect:
                            correct_answer = a.ans
                
                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            # questions is not answered
            else:
                results.append({str(q): 'not answered'})
            
        score_ = round(score * multiplier, 2)
        Activated_Question_Bank.objects.create(question_bank=qb, student=student, score=score_)

        return JsonResponse({'score': score_, 'results': results})

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'