from cProfile import Profile
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Question, Choice

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('polls:index')

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_message = "Your profile was created successfully"
    success_url = reverse_lazy('polls:index')

class DetailView(LoginRequiredMixin,generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(LoginRequiredMixin,generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# class ProfileView(LoginRequiredMixin,generic,DetailView):
#     model = Profile
#     template_name = 'registration.profile.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

