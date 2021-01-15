from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .models import Choice, Question
# Create your views here.
def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("poll:loginpage")

    return render(request,'poll/register.html',{'form':form})
def login_page(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                messages.info(request,'Login in succssfully')
                return redirect("poll:index")
            else:
                messages.error(request,'Login failed. Check username or password')
        else:
            messages.error(request,'Invalid')
    return render(request,'poll/login.html',{'form':form})
def logout_page(request):
    logout(request)
    return redirect("poll:index")
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request,'poll/index.html',context)
def test(request):
    return HttpResponse("This is a test")
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request,'poll/detail.html',{'question':question})
def results(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/results.html', {'question': question})

def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,'poll/detail.html',{'question':question,
        'error_message':"Select an option",})
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))

class IndexView(generic.ListView):
    template_name = 'poll/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'poll/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'poll/results.html'