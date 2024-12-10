from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search_buses', views.search_buses, name='search_buses'),
    path('view_seats/<int:schedule_id>/', views.view_seats, name='view_seats'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
