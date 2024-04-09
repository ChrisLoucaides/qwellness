from django.urls import path
from user_management.views import signup, user_login, dashboard, get_user_info, user_logout, filter_advisors_students

urlpatterns = [
    # Other URL patterns
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('get-user-info/', get_user_info, name='get_user_info'),  # TODO FYP:26 Change endpoint to remove method name
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', user_logout, name='user_logout'),
    path('filter-advisors-students/', filter_advisors_students, name='user_logout')
]
