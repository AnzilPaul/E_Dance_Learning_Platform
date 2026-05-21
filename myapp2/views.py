from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from myapp1.models import Category,DanceStyle,Teacher,Video,Purchase,UserRegInfo
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .forms import CategoryForm, StyleForm, TeacherForm, VideoForm
from django.contrib import messages
MAX_ADMINS = 3
# Create your views here.
def admin_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # 🔥 Count existing admins
        admin_count = User.objects.filter(is_staff=True).count()

        if admin_count >= MAX_ADMINS:
            messages.error(request, "Maximum admin limit reached (3 users only).")
            return redirect('admin_signup')

        # 🔥 Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('admin_signup')
        
        # 🔹 Validate email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('admin_signup')
        
        if password != request.POST.get('confirm_password'):
            messages.error(request, "Passwords do not match.")
            return redirect('admin_signup')


        # 🔹 Create admin user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_staff = True   # IMPORTANT
        user.save()

        messages.success(request, "Admin account created successfully.")
        return redirect('admin_login')
    
    return render(request, 'myapp2/customsignup.html')

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('custom_panel')
        else:
            messages.error(request, "Invalid credentials or not an admin")
            return redirect('admin_login')

    return render(request, 'myapp2/customlogin.html')

@login_required
def custom_panel(request):
    if not request.user.is_staff:
        return redirect('home2')
    
    return render(request, 'myapp2/customadminpanel.html')

# 🔹 Logout
@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# 🔹 Add Category
@login_required
def add_category(request):
    if not request.user.is_staff:
        return redirect('home2')

    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Category added successfully")
        return redirect('custom_panel')

    return render(request, 'myapp2/form.html', {'form': form, 'title': 'Add Category'})


# 🔹 Add Style
@login_required
def add_style(request):
    if not request.user.is_staff:
        return redirect('home2')

    form = StyleForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Style added successfully")
        return redirect('custom_panel')

    return render(request, 'myapp2/form.html', {'form': form, 'title': 'Add Style'})


# 🔹 Add Teacher
@login_required
def add_teacher(request):
    if not request.user.is_staff:
        return redirect('home2')

    form = TeacherForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Teacher added successfully")
        return redirect('custom_panel')

    return render(request, 'myapp2/form.html', {'form': form, 'title': 'Add Teacher'})


# 🔹 Add Video
@login_required
def add_video(request):
    if not request.user.is_staff:
        return redirect('home2')

    form = VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Video added successfully")
        return redirect('custom_panel')

    return render(request, 'myapp2/form.html', {'form': form, 'title': 'Add Video'})

@login_required
def video_list(request):
    if not request.user.is_staff:
        return redirect('home2')

    videos = Video.objects.all()
    return render(request, 'myapp2/video_list.html', {'videos': videos})

@login_required
def edit_video(request, id):
    if not request.user.is_staff:
        return redirect('home2')
    video = get_object_or_404(Video, id=id)

    form = VideoForm(request.POST or None, request.FILES or None, instance=video)

    if form.is_valid():
        form.save()
        messages.success(request, "Video edited successfully")
        return redirect('video_list')

    return render(request, 'myapp2/form.html', {'form': form, 'title': 'Edit Video'})

@login_required
def delete_video(request, id):
    if not request.user.is_staff:
        return redirect('home2')

    video = get_object_or_404(Video, id=id)
    video.delete()
    messages.success(request, "Video deleted successfully")
    return redirect('video_list')