from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Poll(models.Model):
    subject = models.CharField(max_length=100, blank=False)
    detail = models.TextField(blank=False)
    picture = models.ImageField(default="polls/default.png", upload_to='polls/')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    password = models.CharField(max_length=100, blank=False)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    def is_available(self):
        if timezone.now() >= self.end_date:
            self.is_active = False
            self.save()
        return self.is_active

class Poll_Choice(models.Model):
    subject = models.CharField(max_length=100, blank=False)
    image = models.ImageField(default='choices/default.png', upload_to='choices/')
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)

class Poll_Vote(models.Model):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_id = models.ForeignKey(Poll_Choice, on_delete=models.CASCADE)
    vote_by = models.ForeignKey(User, on_delete=models.CASCADE)
