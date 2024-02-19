from django.urls import path
from user_management.views import signup, user_login, dashboard

urlpatterns = [
    # Other URL patterns
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
]
