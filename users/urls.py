'''为应用程序users定义URL模式'''

from django.urls import path,include

from . import views

app_name='users'
urlpatterns=[
    #包含默认身份验证的URL。
    path('',include('django.contrib.auth.urls')),
    #注册页面
    path('register/', views.register,name='register'),
]