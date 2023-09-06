from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('course', views.course, name='course'),
    path('blog', views.blog, name='blog'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('reset', views.reset, name='reset'),
    path('change-password/<token>/<uidb64>/',
         views.change_password, name='change_password'),
    path('student', views.student, name='student'),

]
