from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Poll, Poll_Vote, Poll_Choice
from datetime import datetime
from django.utils import timezone
import pygal

@login_required(login_url='login')
def index(request):
    user = request.user

    # Add poll list
    start_polls = Poll.objects.all().order_by('-start_date')
    end_polls = Poll.objects.all().order_by('-end_date')
    available, closed = [], []
    for poll in start_polls:
        if poll.is_available():
            available.append(poll)
    for poll in end_polls:
        if not poll.is_available():
            closed.append(poll)

    # Send context
    context = {
        'fname' : user.first_name,
        'lname' : user.last_name,
        'available' : available,
        'closed' : closed
    }

    return render(request, template_name='polls/index.html', context=context)


@login_required(login_url='login')
def create_poll(request):
    user = request.user

    # GET detail in form
    if request.method == 'POST':
        subject = request.POST.get('subject').strip()
        detail = request.POST.get('detail').strip()
        try:
            picture = request.FILES['picture']
        except:
            picture = None
        start_date = datetime.strptime(request.POST.get('sdate'), '%d/%m/%Y %H:%M')
        end_date = datetime.strptime(request.POST.get('edate'), '%d/%m/%Y %H:%M')
        password = request.POST.get('password').strip()

        # Add poll to DB
        poll = Poll(
                subject = subject,
                detail = detail,
                start_date = start_date,
                end_date = end_date,
                password = password,
                create_by = user
        )
        if picture != None:
            poll.picture = picture
        poll.save()

        return redirect('my_poll')

    # Send Context
    context = {
        'fname' : user.first_name,
        'lname' : user.last_name
    }

    return render(request, 'polls/create.html', context=context)


@login_required(login_url='login')
def delete_poll(request, poll_id):
    user = request.user

    # Get poll by id and delete poll
    poll = Poll.objects.get(id=poll_id)
    if poll.create_by == user:
        poll.delete()

    return redirect('my_poll')


@login_required(login_url='login')
def poll_detail(request, poll_id):
    user = request.user

    # Get poll detail by id
    poll = Poll.objects.get(id=poll_id)

    # Check own
    own = True
    if user != poll.create_by:
        own = False

    # If check password before vote
    passed = True
    msg = ""

    # If check password before view poll
    # passed = False
    # msg = ""
    # sentpass = request.GET.get('password')
    # if poll.password == sentpass or poll.password == "":
    #     passed = True
    # elif poll.password != sentpass and sentpass is not None:
    #     msg = "Password incorrect!"

    # Check not-open poll
    not_open = False
    if timezone.now() < poll.start_date:
        not_open = True

    # Get all choice in poll
    choices = poll.poll_choice_set.all()

    # Send context
    context = {
        'fname' : user.first_name,
        'lname' : user.last_name,
        'picture' : poll.picture.url,
        'sdate' : poll.start_date,
        'edate' : poll.end_date,
        'create_by' : poll.create_by,
        'subject' : poll.subject,
        'detail' : poll.detail,
        'passed' : passed,
        'id' : poll_id,
        'status' : poll.is_active,
        'owned' : own,
        'error' : msg,
        'all_choice' : choices,
        'is_active' : poll.is_active,
        'not_open' : not_open
    }

    # Check vote status
    check_vote = False
    votes = poll.poll_vote_set.all()
    for vote in votes:
        if vote.vote_by == request.user:
            check_vote = True
            context['check_vote'] = vote.choice_id.subject
            break

    # Create pygal graph
    if not poll.is_available() or check_vote:
        pie_chart = pygal.Pie()
        pie_chart.title = f"Result of {poll.subject}"
        for choice in choices:
            pie_chart.add(choice.subject, choice.poll_vote_set.all().count())
            context['graph'] = pie_chart.render().decode('utf-8')

    return render(request, 'polls/detail.html', context=context)


@login_required(login_url='login')
def edit_poll(request, poll_id):
    user = request.user

    # Get poll detail by id
    poll = Poll.objects.get(id=poll_id)

    # Check permission
    if request.user != poll.create_by:
        return redirect('home')

    # Get detail in form and save to DB
    if request.method == 'POST':
        poll.subject = request.POST.get('subject').strip()
        poll.detail = request.POST.get('detail').strip()
        poll.password = request.POST.get('password').strip()
        poll.end_date = datetime.strptime(request.POST.get('edate'), '%d/%m/%Y %H:%M')
        try:
            picture = request.FILES['picture']
        except:
            picture = None
        if picture != None:
            poll.picture = picture
        poll.save()

        return redirect('poll_detail', poll_id)

    # Get all choice in poll
    choices = poll.poll_choice_set.all()

    # Send context
    context = {
        'fname' : user.first_name,
        'lname' : user.last_name,
        'sdate' : poll.start_date,
        'edate' : poll.end_date,
        'subject' : poll.subject,
        'detail' : poll.detail,
        'password' : poll.password,
        'picture' : poll.picture,
        'id' : poll_id,
        'status' : poll.is_active,
        'all_choice' : choices
    }

    return render(request, 'polls/edit.html', context=context)


@login_required(login_url='login')
def close_poll(request, poll_id):
    user = request.user

    # Get poll detail by id
    poll = Poll.objects.get(id=poll_id)

    # Check status
    if poll.create_by == user and poll.is_active == True:
        poll.is_active = False
        poll.end_date = timezone.now()
        poll.save()
        return redirect('poll_detail', poll_id)

    return redirect('my_poll')


@login_required(login_url='login')
def add_choice(request, poll_id):
    user = request.user

    # Get poll detail by id
    poll = Poll.objects.get(id=poll_id)

    # Check permission
    if user != poll.create_by:
        return redirect('home')

    # Get detail in form
    if request.method == 'POST':
        subject = request.POST.get('subject').strip()
        try:
            image = request.FILES['image']
        except:
            image = None

        # Add choice to DB
        choice = Poll_Choice(
            subject = subject,
            poll_id = poll
        )
        if image != None:
            choice.image = image
        choice.save()

        return redirect('edit_poll', poll.id)

    # Send Context
    context = {
        'fname' : user.first_name,
        'lname' : user.last_name,
        'id' : poll_id
    }

    return render(request, 'polls/add_choice.html', context=context)


@login_required(login_url='login')
def delete_choice(request, choice_id):
    user = request.user

    # Get choice by id and delete
    choice = Poll_Choice.objects.get(id=choice_id)
    poll = choice.poll_id
    if user != poll.create_by:
        return redirect('home')
    choice.delete()

    return redirect('edit_poll', poll.id)


@login_required(login_url='login')
def vote_choice(request, choice_id):
    user = request.user

    # Get choice and poll by id
    choice = Poll_Choice.objects.get(id=choice_id)
    poll = choice.poll_id

    # Check vote
    votes = user.poll_vote_set.all()
    for vote in votes:
        if vote.poll_id == poll:
            return redirect('poll_detail', poll.id)

    # Check status
    if not poll.is_available():
        return redirect('poll_detail', poll.id)

    # Add vote status to DB
    if poll.password == '':
        vote = Poll_Vote.objects.create(
            poll_id=poll,
            choice_id=choice,
            vote_by=request.user
        )
    else:
        password = request.POST.get('password')
        if password is None:
            return render(request, 'polls/detail.html', context={'passed': False, 'choice': choice, 'msg': ''})
        else:
            if password == poll.password:
                vote = Poll_Vote.objects.create(
                    poll_id=poll,
                    choice_id=choice,
                    vote_by=request.user
                )
            else:
                return render(request, 'polls/detail.html', context={'passed': False, 'choice': choice, 'msg': 'Password incorrect!'})

    return redirect('poll_detail', poll.id)
