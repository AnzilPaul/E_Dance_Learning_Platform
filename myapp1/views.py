from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import Category,DanceStyle,Teacher,Video,Purchase,UserRegInfo
from django.contrib.auth.models import User
from .forms import UserForm
from .forms import UserRegInfoForm
import razorpay
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import EditProfileForm


#
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home1(request):
    #return HttpResponse("this is homepage")
    return render(request,"myapp1/Home.html")



def register(request):
    registered=False

    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        register_form=UserRegInfoForm(data=request.POST)

        if user_form.is_valid() and register_form.is_valid():
            user=user_form.save(commit=False)
            #Encrypt password
            user.set_password(user_form.cleaned_data['password'])
            #Split full name into first and last name
            full_name=user_form.cleaned_data['full_name']
            parts=full_name.split(" ", 1)
            user.first_name=parts[0]
            if len(parts) > 1:
                user.last_name=parts[1]
            user.save()

            profile2=register_form.save(commit=False)
            profile2.user=user
            profile2.save()

            registered=True
        else:
            print(user_form.errors, register_form.errors)
    else:
        user_form=UserForm()
        register_form=UserRegInfoForm()
    return render(request,"myapp1/Signup.html",context={'user_form':user_form, 'register_form':register_form, 'registered':registered})
def user_login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user_obj=User.objects.get(email=email)
            username=user_obj.username
        except User.DoesNotExist:
            username=None

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home2'))
                #return redirect('myapp1:home2')
            else:
                return HttpResponse("Your account is inactive.")
        else:
            print("Login failed")
            print("Invalid login details")
            return render(request,"myapp1/Login2.html")
    else:
        return render(request,"myapp1/Login.html")
@login_required
def home2(request):
    categories = Category.objects.all()
    return render(request,"myapp1/Dashboard.html",{'categories': categories})

@login_required
def styles(request, category_id):
    styles = DanceStyle.objects.filter(category_id=category_id)
    return render(request, 'myapp1/styles.html', {'styles': styles})

@login_required
def teachers(request, style_id):
    teachers = Teacher.objects.filter(style_id=style_id)
    return render(request, 'myapp1/teachers.html', {'teachers': teachers})

@login_required
def videos(request, teacher_id):
    videos = Video.objects.filter(teacher_id=teacher_id)

    # Check if user purchased this teacher
    purchased = Purchase.objects.filter(
        user=request.user,
        teacher_id=teacher_id,
        is_paid=True
    ).exists()

    return render(request, 'myapp1/videos.html', {
        'videos': videos,
        'purchased': purchased
    })



@login_required
def create_payment(request, teacher_id):
    amount = 1  # ₹1

    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    order = client.order.create({
        "amount": amount * 100,  # paise
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request, "myapp1/payment.html", {
        "key_id": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "order_id": order['id'],
        "teacher_id": teacher_id
    })



    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home1'))
    #return redirect('myapp1:home1')

@login_required
def verify_payment(request):
    if request.method == "POST":
        try:
            # 🔹 Get data from frontend
            data = json.loads(request.body)

            payment_id = data.get("payment_id")
            order_id = data.get("order_id")
            signature = data.get("signature")
            teacher_id = data.get("teacher_id")

            # 🔹 Initialize Razorpay client
            client = razorpay.Client(auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            ))

            # 🔐 Verify payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            # 🔹 Get teacher object
            teacher = Teacher.objects.get(id=teacher_id)

            # 🔹 Save purchase (IMPORTANT LINE)
            Purchase.objects.get_or_create(
                user=request.user,
                teacher=teacher,
                defaults={'is_paid': True}
            )

            # ✅ Success response
            return JsonResponse({"status": "success"})

        except Teacher.DoesNotExist:
            return JsonResponse({"status": "failure", "message": "Teacher not found"})

        except Exception as e:
            return JsonResponse({"status": "failure", "message": str(e)})

    return JsonResponse({"status": "invalid request"})

def about(request):
    return render(request,"myapp1/Aboutus.html")

def contact(request):
    return render(request,"myapp1/Contactus.html")

@login_required
def profile_view(request):
     user = request.user
     return render(request, "myapp1/profile.html", {'user':user})

@login_required
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = EditProfileForm(instance=user)

    return render(request, "myapp1/editprofile.html", {'form': form})

@login_required
def change_password(request):
    user = request.user

    if request.method == "POST":
        form2 = PasswordChangeForm(user, request.POST)
        if form2.is_valid():
            form2.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect("/profile/")
    else:
        form2 = PasswordChangeForm(user)

    return render(request, "myapp1/changepassword.html", {'form2':form2})

def privacy(request):
    return render(request, "myapp1/privacy.html")

def terms(request):
    return render(request, "myapp1/terms.html")



def refund(request):
    return render(request, "myapp1/refund.html")

def shipping(request):
    return render(request, "myapp1/shipping.html")