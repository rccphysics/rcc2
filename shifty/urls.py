from django.urls import path

from . import views

app_name = 'shifty'
urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.list, name='list'),
    path('add_form', views.add_form, name='add_form'),
    path('add', views.add, name='add'),
    path('<int:mrn>/', views.view_patient, name='view_patient')
]
