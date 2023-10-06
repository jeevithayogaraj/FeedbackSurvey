from django.urls import path
from . import views


urlpatterns = [
    path('',views.custom_login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('signup/',views.signup,name='signup'),
    path('email/',views.email_temp,name='email_temp'),
    path('form/',views.form,name='form'),
    path('success/',views.successful,name='successful'),
    path('reports/',views.review_list,name='reviews'),
    path('today-report/', views.fetch_data_for_today, name='fetch_data_for_today'),
    path('week-report/', views.fetch_data_for_week, name='fetch_data_for_week'),
    path('month-report/', views.fetch_data_for_month, name='fetch_data_for_month'),
    path('overall-report/', views.fetch_overall_report, name='fetch_overall_report'),
    path('base/',views.base,name='base'),
    path('download-excel/', views.download_excel, name='download_excel'),
    ]