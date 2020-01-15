from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from whitebricks.forms import SignupForm, LoginForm, PGForm
from django.contrib.auth.decorators import login_required
from whitebricks.models import PG
from django.contrib import messages
from django.db.models import Q
from django.core import serializers
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .tokens import account_activation_token



def index(request):
    signup_form = SignupForm(request.POST)
    return render(request, 'whitebricks/index.html', {"form": signup_form})

@login_required()
def yourads(request):
    signup_form = SignupForm(request.POST)
    results = PG.objects.filter(created_by=request.user.id)

    context = {"form": signup_form,
               "pgs": results}
    return render(request, 'whitebricks/yourads.html', context)



def about(request):
    signup_form = SignupForm(request.POST)
    return render(request, 'whitebricks/about.html', {"form": signup_form})



def adspace(request):
    signup_form = SignupForm(request.POST)
    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups = Q(city__icontains=query)

            results = PG.objects.filter(lookups).distinct()


            context = {'pgs': results,
                       'submitbutton': submitbutton,
                       'form': signup_form}

            return render(request, 'whitebricks/adspace.html', context)

        else:
            pg_form = PGForm(request.GET)
            return render(request, 'whitebricks/adspace.html', {'form2': pg_form, "form": signup_form})

    else:
        pg_form = PGForm(request.GET)
        return render(request, 'whitebricks/adspace.html', {'form2': pg_form, "form": signup_form})



def signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data['username']
            email = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                return HttpResponse("Username/Email Already Exists")
            else:

                user = User.objects.create_user(username, email, password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate Your MySite Account'
                message = render_to_string('whitebricks/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
                return redirect('account_activation_sent')
    else:
        signup_form = SignupForm(request.POST)
    return render(request, 'whitebricks/index.html', {"form": signup_form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        auth_login(request, user)
        return redirect('/whitebricks')
    else:
        return render(request, 'whitebricks/account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'whitebricks/account_activation_sent.html')


def login(request):

    if request.user.is_authenticated:
        return HttpResponse('You Are already logged in')
    else:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():

                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']

                user = authenticate(username=username, password=password)

                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        return redirect('/whitebricks')
                    else:
                        return HttpResponse('Your account is not active')
                else:
                    return HttpResponse('The Account does not exists')
            else:
                login_form = LoginForm()
                return render(request, "blog/login.html", {"form": login_form})
        else:
            login_form = LoginForm()
        return render(request, 'whitebricks/index.html', {"form": login_form})




def logout_view(request):
    logout(request)
    return redirect('/whitebricks')


@login_required()
def insert_PG(request):
    if request.method == 'POST':

        pg_form = PGForm(request.POST, request.FILES)
        if pg_form.is_valid():
            highlights_pg = pg_form.cleaned_data['info_highlights']
            description_pg = pg_form.cleaned_data['info_description']
            price_pg = pg_form.cleaned_data['info_price']
            bedroom_pg = pg_form.cleaned_data['info_bedroom']
            city_pg = pg_form.cleaned_data['info_city']
            image_pg = request.FILES['info_image']
            fname_user = pg_form.cleaned_data['info_fname']
            lname_user = pg_form.cleaned_data['info_lname']
            email_user = pg_form.cleaned_data['info_email']
            phone_user = pg_form.cleaned_data['info_phone']
            address_user = pg_form.cleaned_data['info_address']

            object1 = PG(highlights=highlights_pg, description=description_pg, price=price_pg,
                         bedroom=bedroom_pg, city=city_pg, image=image_pg,
                         first_name=fname_user, last_name=lname_user, email=email_user,
                         phone=phone_user, address=address_user)
            object1.created_by=request.user.id
            object1.save()  # will save the data from the form to database

            messages.success(request, 'PG posted !')
            return redirect('/whitebricks')
        else:
            return HttpResponse('invalid')


    else:
        pg_form = PGForm(request.POST)
        return render(request, 'whitebricks/pginfo.html', {'form2': pg_form})




def delete(request):
    your_parameter = request.GET['parameter']
    owner_info=PG.objects.filter(id=your_parameter)
    owner_info.delete()
    messages.error(request, 'PG deleted !')
    return redirect('/whitebricks')

def edit(request):
    your_parameter = request.GET['parameter']
    if request.method == 'POST':

        pg_form = PGForm(request.POST, request.FILES)
        if pg_form.is_valid():
            owner_info = PG.objects.get(id=your_parameter)
            owner_info.highlights = pg_form.cleaned_data['info_highlights']
            owner_info.description = pg_form.cleaned_data['info_description']
            owner_info.price = pg_form.cleaned_data['info_price']
            owner_info.bedroom = pg_form.cleaned_data['info_bedroom']
            owner_info.city = pg_form.cleaned_data['info_city']
            owner_info.image = request.FILES['info_image']
            owner_info.first_name = pg_form.cleaned_data['info_fname']
            owner_info.last_name = pg_form.cleaned_data['info_lname']
            owner_info.email = pg_form.cleaned_data['info_email']
            owner_info.phone = pg_form.cleaned_data['info_phone']
            owner_info.address = pg_form.cleaned_data['info_address']


            owner_info.save()  # will save the data from the form to database

            messages.success(request, 'PG posted !')
            return redirect('/whitebricks')
        else:
            return HttpResponse('invalid')

    else:
        owner_info=PG.objects.get(id=your_parameter)
        pg_form = PGForm(initial={"info_highlights":owner_info.highlights,
                                  "info_description":owner_info.description,
                                  "info_price":owner_info.price,
                                  "info_bedroom":owner_info.bedroom,
                                  "info_city": owner_info.city,
                                  "info_image": owner_info.image,
                                  "info_fname": owner_info.first_name,
                                  "info_lname": owner_info.last_name,
                                  "info_email": owner_info.email,
                                  "info_phone": owner_info.phone,
                                  "info_address": owner_info.address})
        return render(request, 'whitebricks/editPG.html', {"form2": pg_form, "yp": your_parameter})
