from django import forms
from myapp1.models import Category, DanceStyle, Teacher, Video

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class StyleForm(forms.ModelForm):
    class Meta:
        model = DanceStyle
        fields = '__all__'

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = '__all__'