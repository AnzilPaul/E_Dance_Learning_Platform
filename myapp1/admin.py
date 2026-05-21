from django.contrib import admin
from .models import UserRegInfo
from .models import Category, DanceStyle, Teacher, Video, Purchase
# Register your models here.
admin.site.register(UserRegInfo)
admin.site.register(Category)
admin.site.register(DanceStyle)
admin.site.register(Teacher)
admin.site.register(Video)
admin.site.register(Purchase)

