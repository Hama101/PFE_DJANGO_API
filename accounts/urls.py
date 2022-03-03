from . import views as v
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    #users
    path('signup/',v.signup,name="signup"),
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