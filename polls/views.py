from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question, Choice, Profile
from django.contrib.auth.models import User
from .forms import UserForm, ProfileForm
from django.db import transaction

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('polls:index')

class UserProfileView(generic.UpdateView):
    form_class = UserChangeForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('polls:index')

    def get_object(self):
        return self.request.user

class UserEditView(generic.UpdateView):
    form_class = UserForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('polls:index')

    def get_object(self):
        return self.request.user

# def update_profile(request, user_id):
#     user = User.objects.get(pk=user_id)
#     user.profile.bio = 
#     user.profile.age = 
#     user.profile.birth_date = 

def edit_profile(request):
    submitted = False
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/edit_profile?submitted=True')
    else:
        form = ProfileForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'registration/edit_profile.html',{
        'form':form,
        'submitted':submitted,
        })

@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success = (request, ('Your profile was successfully updated!'))
            return reverse_lazy('profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# def edit_profile(request):
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

#         if form.is_valid() and profile_form.is_valid():
#             user_form = form.save()
#             custom_form = profile_form.save(False)
#             custom_form.user = user_form
#             custom_form.save()
#             return reverse_lazy('polls:index')
#         else:
#             form = EditProfileForm(instance=request.user)
#             profile_form = ProfileForm(instance=request.userprofile)
#             args = {}
#             args['form'] = form
#             args['profile_form'] = profile_form
#             return render(request, 'registration/edit_profile.html', args)

# def edit_profile(request, template_name="registration/edit_profile.html"):
#     if request.method == "POST":
#         form = UserForm(data=request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#             url = reverse_lazy('profile')
#             return HttpResponseRedirect(url)
#         else:
#             form=UserForm(instance=request.user)
#         page_title = _('Edit Profile')
#         return render_to_response(template_name, locals()),
#             context_instance=RequestContext(request))
# class UserEditView(generic.CreateView):
#     form_class = UserChangeForm
#     template_name

# class ProfileView(LoginRequiredMixin,generic.DetailView):
#     model = Profile
#     template_name = 'registration/profile.html'

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

# def registerPage(request):
#     form = UserCreationForm

#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()


class DetailView(LoginRequiredMixin,generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(LoginRequiredMixin,generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()


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