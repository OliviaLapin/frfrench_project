from django.urls import path
from . import views

app_name = 'french'

urlpatterns = [
    path('', views.home, name='home'),
    path('topics/', views.topics_list, name='topics'),
    path('quiz/<int:topic_id>/', views.quiz, name='quiz'),
   path('card/add/', views.card_add, name='add_card'),
    path('card/edit/<int:card_id>/', views.edit_card, name='edit_card'),
    path('stats/', views.stats, name='stats'),
    path('send-card/', views.send_card, name='send_card'),
]
