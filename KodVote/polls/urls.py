from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # poll
    path('', views.poll_index, name='home'),
    path('poll_create/', views.poll_create, name='create'),
    path('poll_delete/<int:poll_id>', views.poll_delete, name='poll_delete'),
    # path('poll_detail/<int:poll_id>', views.poll_detail, name='poll_detail'),
    # path('poll_edit/<int:poll_id>', views.poll_edit, name='poll_edit'),
    # path('poll_close/<int:poll_id>', views.poll_close, name='poll_close'),
    # path('poll_vote/<int:choice_id>', views.poll_vote, name='poll_vote'),

    # choice
    # path('choice_add/<int:poll_id>', views.choice_add, name='choice_add'),
    # path('choice_delete/<int:choice_id>', views.choice_delete, name='choice_delete')
]
