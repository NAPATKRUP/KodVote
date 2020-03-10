from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from .models import Poll, Poll_Vote, Poll_Choice
from datetime import datetime
from django.utils import timezone

@login_required
def index(request):
    user = request.user
    polls = Poll.objects.all().order_by('start_date')
    available, closed = [], []
    for poll in polls:
        if poll.is_available():
            available.append(poll)
        else:
            closed.append(poll)
    context = {
        'fname' : user.first_name,
        'lname' : user.last_name,
        'available' : available,
        'closed' : closed
    }
    return render(request, template_name='polls/index.html', context=context)

@login_required
def create_poll(request):
    user = request.user
    if request.method == 'POST':
        subject = request.POST.get('subject')
        detail = request.POST.get('detail')
        try:
            picture = request.FILES['picture']
        except:
            picture = None
        start_date = datetime.strptime(request.POST.get('sdate'), '%d/%m/%Y %H:%M')
        end_date = datetime.strptime(request.POST.get('edate'), '%d/%m/%Y %H:%M')
        password = request.POST.get('password').strip()
        poll = Poll(
                subject=subject,
                detail=detail,
                start_date=start_date,
                end_date=end_date,
                password=password,
                create_by=user
        )
        if picture != None:
            poll.picture = picture
        poll.save()
        return redirect('home')
    context = {
        'fname' : user.first_name,
        'lname' : user.last_name
    }
    return render(request, 'polls/create.html', context=context)

@login_required
def delete_poll(request, poll_id):
    user = request.user
    poll = Poll.objects.get(id=poll_id)
    if poll.create_by == user:
        poll.delete()
    return redirect('my_poll')

@login_required
def poll_detail(request, poll_id):
    user = request.user
    poll = Poll.objects.get(id=poll_id)
    own = True
    passed = False
    msg = ""
    if user != poll.create_by:
        own = False

    sentpass = request.GET.get('password')
    if poll.password == sentpass or poll.password == "":
        passed = True
    elif poll.password != sentpass and sentpass is not None:
        msg = "Password incorrect"

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
        'error' : msg
    }
    return render(request, 'polls/detail.html', context=context)

@login_required
def edit_poll(request, poll_id):
    user = request.user
    poll = Poll.objects.get(id=poll_id)
    if request.user != poll.create_by:
        return redirect('home')
    if request.method == 'POST':
        poll.subject = request.POST.get('subject')
        poll.detail = request.POST.get('detail')
        poll.password = request.POST.get('password').strip()
        poll.save()
        return redirect('poll_detail', poll_id)
    context = {
        'fname' : user.first_name,
        'lname' : user.last_name,
        'sdate' : poll.start_date,
        'edate' : poll.end_date,
        'subject' : poll.subject,
        'detail' : poll.detail,
        'id' : poll_id,
        'status' : poll.is_active
    }
    return render(request, 'polls/edit.html', context=context)

@login_required
def close_poll(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    if poll.create_by == request.user and poll.is_active == True:
        poll.is_active = False
        poll.end_date = timezone.now()
        poll.save()
    return redirect('my_poll')
