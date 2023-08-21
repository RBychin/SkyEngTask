from django.urls import path

from allauth.account.views import LoginView, LogoutView, SignupView
from . import views
from .views import PyFileDetailView

app_name = 'web'

urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),
    path('upload/', views.FileUpload.as_view(), name='upload_files'),
    path('view_py_file/<int:pk>/update/', views.FileUpdate.as_view(), name='update_files'),
    path('view_py_file/<int:pk>/', PyFileDetailView.as_view(), name='view_py_file'),
    path('view_py_file/<int:pk>/del/', views.FileDelete.as_view(), name='file_delete'),
    path('myfiles/', views.ProfileIndex.as_view(), name='self_files'),
    path('', views.FilesIndex.as_view(), name='main')
]
