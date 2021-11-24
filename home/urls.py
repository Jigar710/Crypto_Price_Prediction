from django.contrib import admin
from django.urls import path,include
from home import views
from crypto import settings
# if settings.DEBUG:
#     urlpatterns += [url(r'^static/(?P<path>.*)$', views.serve),]

urlpatterns = [
    path("",views.index,name='index'),
    path("index",views.index,name='index2'),
    path("home",views.home,name='home'),
    path("about",views.about,name='about'),
    path("profile",views.profile,name='profile'),
    path("contact",views.contact,name='contact'),
    path("login",views.login1,name='login'),
    path("logout",views.logout1,name='logout'),
    # path("current",views.current,name='current'),
    path("accuracy",views.accuracy,name='accuracy'),
    path("collect",views.collect,name='collect'),
    path("prediction",views.prediction,name='prediction'),
    path("prediction2",views.prediction2,name='prediction2'),
    path("signup",views.signup1,name='signup'),
    path("news",views.news,name='news'),
    path("reload",views.reload,name='reload'),

]
