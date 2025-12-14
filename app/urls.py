from django.urls import path
from . import views

urlpatterns=[
    path('',views.home_view,name='home'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('signup/',views.signup_view,name='signup'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('capsule/create/', views.create_capsule, name='create_capsule'),
    path('capsules/', views.capsule_list, name='capsule_list'),
    path('capsules/<str:capsule_id>/', views.capsule_detail, name='capsule_detail'),
    path('capsules/<str:capsule_id>/collaborators/',views.manage_collaborators,name='manage_collaborators'),
    path('capsules/<str:capsule_id>/entry/',views.add_entry,name='add_entry'),
    path('capsules/<str:capsule_id>/trigger-event/',views.trigger_event,name='trigger_event'),
    path('notifications/', views.notifications, name='notifications'),
    path('api/notifications/count/', views.notification_count_api, name='notification_count_api'),


]