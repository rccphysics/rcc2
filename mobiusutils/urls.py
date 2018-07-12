from django.urls import path

from . import views

app_name = 'mobiusutils'
urlpatterns = [
    path('list/', views.list, name='list'),
]
