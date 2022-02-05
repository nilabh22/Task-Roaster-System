from django.urls import path
from . import views


app_name = 'taskapp'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', views.loginPage, name = 'login'),
    path('user/',views.userPage,name='user-page'),
    path('register/', views.registerPage, name = 'register'),
    path('logout/',views.logoutUser, name='logout'),
    path('createTask', views.createTask, name = 'createTask'),
    path('editTask/<int:pk>', views.editTask, name = 'editTask'),
    path('deleteTask/<int:pk>', views.deleteTask, name='deleteTask'),
    path('viewTask/<int:pk>', views.viewTask, name = 'viewTask'),
]
