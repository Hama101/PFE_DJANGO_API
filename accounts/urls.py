from . import views as v
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    #users
    path('signup/',v.signup,name="signup"),
    
    #profiles
    path('profiles-list/',v.profiles_list,name="profiles-list"),
    path('profile/<str:username>/',v.profile,name="profile"),
    path('update-profile/',v.update_profile ,name="update-profile"),

]

from knox import views as knox_views
from .views import LoginAPI
from django.urls import path

urlpatterns += [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('user/',v.UserAPI().as_view(),name="user"),
]

#jwt
urlpatterns += [
    path('register/', v.RegisterView.as_view()),
    path('user/', v.LoadUserView.as_view()),
]