from django.urls import path

from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('test', views.test, name='test'),
    path('<int:question_id>/', views.detail, name='detail'),
]