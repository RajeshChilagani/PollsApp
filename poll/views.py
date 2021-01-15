from django.shortcuts import HttpResponse
from django.template import loader

from .models import Choice, Question
# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('poll/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context,request))
def test(request):
    return HttpResponse("This is a test")
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)