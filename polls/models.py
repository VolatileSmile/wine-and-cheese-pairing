import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Profile(models.Model):
    user = models.OneToOneField(User, default="Username", null=True, on_delete=models.CASCADE)
    #slug = models.SlugField(max_length = 250, null = True, blank = True)
    avatar = models.ImageField(blank=True, null=True, upload_to="images/") #holy shit i did it boys
    bio = models.TextField(max_length=500, blank=True, default="This is a default bio")
    age = models.CharField(max_length=3, blank=True, default="69")
    birth_date = models.DateField(null=True, blank=True, default="2001-09-11")

    def __str__(self):
        return str(self.user)

# def createProfile(sender, **kwargs):
#     if kwargs['created']:
#         user_profile = Profile.objects.created(user=kwargs['instance'])
#         post_save.connect(createProfile, sender=User)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# @receiver(post_save, sender=User)
# def post_save_receiver(sender, instance, *args, **kwargs):
#    if not instance.slug:
#        instance.slug = unique_slug_generator(instance)