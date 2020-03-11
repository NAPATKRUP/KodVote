from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

class Poll(models.Model):
    subject = models.CharField(max_length=255, blank=False, null=False)
    detail = models.TextField(blank=False, null=False)
    picture = models.ImageField(default="polls/default.png", upload_to='polls/')
    start_date = models.DateTimeField(default=datetime.now, blank=False, null=False)
    end_date = models.DateTimeField(blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    def is_available(self):
        if (timezone.now() >= self.end_date) or (timezone.now() < self.start_date):
            self.is_active = False
            self.save()
        else:
            self.is_active = True
            self.save()
        return self.is_active

class Poll_Choice(models.Model):
    subject = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(default='choices/default.png', upload_to='choices/')
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)

class Poll_Vote(models.Model):
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_id = models.ForeignKey(Poll_Choice, on_delete=models.CASCADE)
    vote_by = models.ForeignKey(User, on_delete=models.CASCADE)
