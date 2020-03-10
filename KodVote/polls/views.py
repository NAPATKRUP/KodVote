from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from .models import Poll, Poll_Vote, Poll_Choice
from datetime import datetime

@login_required
def poll_index(request):
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
def poll_create(request):
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
def poll_delete(request, poll_id):
    user = request.user
    poll = Poll.objects.get(id=poll_id)
    if poll.create_by == user:
        poll.delete()
    return redirect('my_poll')
