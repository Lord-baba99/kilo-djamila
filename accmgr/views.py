from django.shortcuts import get_object_or_404, render
from accmgr.models import Teacher
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.contrib.auth import logout, login, authenticate, get_user_model, get_user
from accmgr.models import Person
from . forms import *
from django.contrib import messages
from django.utils.translation import gettext as _



User = get_user_model()

BASE_TEMPLATE = 'layouts/base.html'

def logout_user(request):
    logout(request)
    return redirect('login')


def login_user(request):
    # print("Impression de la requete: ", request.POST)
    url=None
    if request.method == 'GET':
        url = request.GET.get('next')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # print(email, password)
        user = authenticate(email=email, password=password)
        
        # print(user)
        if user:
            login(request, user)
            if url:
                return redirect(f'{url}')
            elif not url:
                return redirect('main-home')
        elif user==None:
            return render(request, BASE_TEMPLATE, {'template_name': 'contents/authentication/sign-in.html', 'error_message': 'Nom d\'utilisateur ou mot de passe invalide !'})

    return render(request, BASE_TEMPLATE, {'template_name': 'contents/authentication/sign-in.html'})


def signup(request):
    if request.POST:
        #print('request post')
        username_to_be_validate = request.POST.get('username')
        mail_to_be_validate = request.POST.get('email')
        if username_to_be_validate and mail_to_be_validate:
            #print('validation')
            persons_by_username = Person.objects.filter(username=username_to_be_validate)
            persons_by_email = Person.objects.filter(email=mail_to_be_validate)
            
            if persons_by_email.count() > 0:
                messages.error(request, _(f"This email ({mail_to_be_validate}) is already used"))
            
            if persons_by_username.count() > 0:
                # print("person's count > 0" )
                # print('form invalid 1')
                messages.error(request, _(f"This username ({username_to_be_validate}) is already used"))
            
            #print("test : ", persons_by_email.count() == 0 and persons_by_username.count() == 0)
            if persons_by_email.count() == 0 and persons_by_username.count() == 0:
                #print("person's count == 0" )
                
                form = PersonForm(request.POST)
                if form.is_valid():
                    print('form valid')
                    form.save()
                    email = request.POST.get('email')
                    password = request.POST.get('password')
                    user = authenticate(email=email, password=password)
                    if user:
                        login(request, user, backend='accmgr.auth_features.EmailBackend')
                        messages.success(request, _(f"Welcome {email}, happy to see you !"))
                    context = {
                        'url': reverse('login'),
                        'success': True,
                        'name': 'username',
                        "messages": messages.get_messages(request),
                        'success_message': 'Vous avez été correctement enregistré !'
                    }
                    if user.is_authenticated:
                        return redirect(reverse_lazy('main-home'))
                    else:
                        return redirect(reverse_lazy('login'))

                else:
                    print('form invalid 2')
                    errors = form.errors
                    print(errors)
                    
                    context = {
                    "error": True,
                    "error_message": "Les éléments suivants sont nécessaires :",
                    'url': reverse('signup'),
                    'form': form,
                    'template_name': 'contents/authentication/sign-up.html',
                    }
                    return render(request, BASE_TEMPLATE, context)

            #for x in messages.get_messages(request):
            #    print(x)
                
            context = {
                "template_name": 'contents/authentication/sign-up.html',
                "error": True,
                "messages": messages.get_messages(request),
                "error_message": "Un utilisateur ayant le même nom existe déjà !"
                }
            return render(request, BASE_TEMPLATE, context)
        
    return render(request, BASE_TEMPLATE, {'dateform': JoinedDate(), 'template_name': 'contents/authentication/sign-up.html'})


def make_request(request):
    if request.POST:
        email_to_validate = request.POST.get('email')
        tar = TeacherAccountRequest.objects.filter(email=email_to_validate)
        
        if tar.count() > 0:    
            
            messages.error(request, _("The email provided is already used!"))
            
            context = {
                    "messages": messages.get_messages(request),
                    "provided_email": email_to_validate,
                    "template_name": "contents/authentication/failed-request.html",
                }
                
            return render(request, BASE_TEMPLATE, context)
        
        elif tar.count() == 0:
            form = TeacherAccountRequestForm(request.POST)
            
            if form.is_valid():
                form.save()
                messages.success(request, _("Your request has been send successfully !"))
                
                context = {
                    "messages": messages.get_messages(request),
                    "template_name": "contents/authentication/success-request.html",
                }
                
                return render(request, BASE_TEMPLATE, context)
    
    context = {
        "template_name": "contents/authentication/teacher-sign-up.html"
    }
    return render(request, BASE_TEMPLATE, context)


def signup_teacher(request):
    
    pass


def reset_password(request):
    return render(request, BASE_TEMPLATE, {'template_name': 'contents/authentication/forgot-password.html'})

def show_profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'user_profile.html', context)


def update_profile(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        location = request.POST.get('location')
        niu = request.POST.get('niu')
        profile_picture = request.POST.get('profile_picture')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        driving_licence_picture = request.POST.get('driving_licence_picture')
        driving_licence_number = request.POST.get('driving_licence_number')
        id_card_picture = request.POST.get('id_card_picture')
        id_card_number = request.POST.get('id_card_number')

        requested_user = get_user(request)
        user = Person.objects.filter(id=requested_user.id)
        user.update(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            location=location,
            niu=niu,
            profile_picture=profile_picture,
            gender=gender,
            phone_number=phone_number,
            driving_licence_picture=driving_licence_picture,
            driving_licence_number=driving_licence_number,
            id_card_picture=id_card_picture,
            id_card_number=id_card_number,
        )
        return redirect('profile')
    return redirect('profile')



@staff_member_required
def add_to_premiumGroup(request):
    if request.POST:
        target_user_id = request.POST.get("target_user_id")
        target_user = get_object_or_404(Teacher, id=target_user_id)
        target_group = Group.objects.get(name="Premium")
        target_user.groups.add(target_group)
        return render(request, "success_101.html")


def _create_group(name) -> None:
    group = Group.objects.create(name=name)
    group.save()
    return group
    
@staff_member_required
def create_group(request):
    if request.POST:
        group_name = request.POST.get("group_name")
        _create_group(name=group_name)
        return

def settings(request):
    user = request.user
    settings = UserSettings.objects.get(user_id=user.id)
    
    context = {
        'template_name': 'contents/settings.html',
        'settings': settings,
    }
    return render(request, BASE_TEMPLATE, context)
