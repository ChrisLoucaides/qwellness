from django.urls import path
from user_management.views import signup, user_login, dashboard, get_user_info, user_logout

urlpatterns = [
    # Other URL patterns
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('get-user-info/', get_user_info, name='get_user_info'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', user_logout, name='user_logout')
]
