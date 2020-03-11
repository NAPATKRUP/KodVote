from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from polls.models import Poll

def my_login(request):
    context = {}

    # Get detail in form
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # Success
        if user:
            login(request, user)

            # Redirect
            next_url = request.POST.get('next_url')
            if next_url != '':
                return redirect(next_url)
            else:
                return redirect('home')

        # Fail
        else:
            context['username'] = username
            context['password'] = password
            context['error'] = 'Wrong username or password!'

    # Get url path
    next_url = request.GET.get('next')
    if next_url:
        context['next_url'] = next_url

    return render(request, template_name='management/login.html', context=context)


def register(request):
    context = {}

    # Get detail in form
    if (request.method == 'POST'):
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check already used
        if (User.objects.filter(username=username).exists()):
            context['error'] = 'Username is already used!'
            context['fname'] = first_name
            context['lname'] = last_name
            context['email'] = email
            context['username'] = username
            context['password'] = password
            return render(request, 'management/register.html', context=context)

        # Add user to DB
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        login(request, user)
        return redirect('home')

    return render(request, template_name='management/register.html', context=context)


@login_required(login_url='login')
def my_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def change_password(request):
    user = request.user
    context = {}
    context['username'] = user.username

    # Get detail in form
    if request.method == 'POST':
        password1 = request.POST.get('npass1')
        password2 = request.POST.get('npass2')

        # Check password matching
        if password1 != password2:
            context['error'] = 'Password not match!'
            return render(request, template_name='management/change_password.html', context=context)

        # Set password to DB
        user.set_password(password1)
        user.save()
        logout(request)
        return redirect('login')

    return render(request, template_name='management/change_password.html', context=context)


@login_required(login_url='login')
def my_poll(request):
    user = request.user

    # Get all my poll
    start_polls = Poll.objects.filter(create_by=user).order_by('-start_date')
    end_polls = Poll.objects.filter(create_by=user).order_by('-end_date')
    available, closed = [], []
    for poll in start_polls:
        if poll.is_available():
            available.append(poll)
    for poll in end_polls:
        if not poll.is_available():
            closed.append(poll)

    # Send Context
    context = {
        'fname' : user.first_name,
        'lname' : user.last_name,
        'username' : user.username,
        'email' : user.email,
        'available' : available,
        'closed' : closed
    }

    return render(request, 'management/my_poll.html', context=context)
