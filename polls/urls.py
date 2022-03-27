from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.views import generic
from . import views
from .views import UserEditView, UserProfileView


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #path('profile/', views.ProfileView.as_view(), name='profile'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('accounts/', include('django.contrib.auth.urls')),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(template_name='change-password.html'),
    ),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='polls/login.html')),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name="logout"),
    #path('profile/', views.ProfileView.as_view(template_name="registration/profile.html")),
    #path('accounts/profile/', views.ProfileView.as_view(template_name='registration/profile.html')),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    #path('edit_profile/', views.UserEditView(template_name="registration/edit_profile.html")),
    path("signup/", views.SignUpView.as_view(), name="signup"),

]