from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('directory/', views.directory_view, name='directory'),
    path('signup/', views.signup_view, name='signup'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('import-valid-entries/', views.import_valid_entries, name='import_valid_entries'),
    path('add-valid-entry/', views.add_valid_entry, name='add_valid_entry'),
    path('executive-board/', views.executive_board_view, name='executive_board'),
]
