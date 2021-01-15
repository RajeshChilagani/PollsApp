from django.urls import path

from . import views
app_name = 'poll'
urlpatterns = [
    path('',views.IndexView.as_view(), name='index'),
    path('register/',views.register_page,name='registerpage'),
    path('login/',views.login_page,name='loginpage'),
    path('logout/',views.logout_page,name='logoutpage'),
    path('test', views.test, name='test'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/',views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]