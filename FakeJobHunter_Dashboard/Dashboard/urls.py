from django.urls import path

from . import views

app_name = 'Dashboard'

urlpatterns = [
    path('', views.job_offer_analysis, name='home'),
    path('job_offer_analysis/', views.job_offer_analysis, name='job_offer_analysis'),
    path('overall_analysis/', views.overall_analysis, name='overall_analysis'),
]
