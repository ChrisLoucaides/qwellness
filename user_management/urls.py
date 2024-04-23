from django.urls import path
from django.views.generic import RedirectView

from user_management.views import signup, user_login, get_user_info, user_logout, filter_advisors_students

urlpatterns = [
    # Other URL patterns
    path('', RedirectView.as_view(url='/login', permanent=False)),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('user-info/', get_user_info, name='user_info'),
    path('logout/', user_logout, name='user_logout'),
    path('filter-advisors-students/', filter_advisors_students, name='user_logout')
]
