from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # poll
    path('', views.index, name='home'),
    path('create_poll/', views.create_poll, name='create'),
    path('delete_poll/<int:poll_id>', views.delete_poll, name='delete_poll'),
    path('poll_detail/<int:poll_id>', views.poll_detail, name='poll_detail'),
    path('edit_poll/<int:poll_id>', views.edit_poll, name='edit_poll'),
    path('close_poll/<int:poll_id>', views.close_poll, name='close_poll'),
    # path('vote_poll/<int:choice_id>', views.vote_poll, name='vote_poll'),

    # choice
    # path('add_choice/<int:poll_id>', views.add_choice, name='add_choice'),
    # path('delete_choice/<int:choice_id>', views.delete_choice, name='delete_choice')
]
