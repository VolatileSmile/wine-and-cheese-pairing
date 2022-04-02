import datetime
from django.contrib import admin
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #id = models.OneToOneField(User, primary_key=True, db_column="id", on_delete=models.CASCADE)
    #slug = models.SlugField(blank=True, null=True)
    name = models.CharField(verbose_name="name", max_length=200, blank=True)
    avatar = models.ImageField(verbose_name="avatar", blank=True, null=True, upload_to="images/")
    bio = models.TextField(verbose_name="bio", max_length=500, blank=True)
    age = models.CharField(verbose_name="age", max_length=3, blank=True)
    birthday = models.DateField(verbose_name="birthday", null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, force_insert=False, **kwargs):
        if self.pk is None or force_insert:
            Profile.objects.filter(user_id=self.user_id).delete()
        return super().save(*args, force_insert=force_insert, **kwargs)

    #def save(self, *args, **kwargs):
        #self.slug = slugify(self.name, self.avatar, self.bio, self.age, self.birthday)
        #super().save(*args, **kwargs)
        #if self.slug is None:
            #self.slug = slugify(self.name, self.avatar, self.bio, self.age, self.birthday)
            #self.save()


    def updateUserProfile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()