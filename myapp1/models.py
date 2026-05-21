from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserRegInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number=models.CharField(max_length=15,unique=True,blank=False,null=False)
    home_address=models.TextField(blank=True)
    def __str__(self) -> str:
        return self.user.username

# Dance Category (Classical, Western)
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Dance Style (Kathakali, Kuchipudi)
class DanceStyle(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Teacher
class Teacher(models.Model):
    style = models.ForeignKey(DanceStyle, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Video
class Video(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/')
    is_free = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


# Payment Unlock
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.teacher}"