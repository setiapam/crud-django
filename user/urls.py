from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('add_user/', views.add_user, name='add_user'),
    path('update_user/<str:pk>', views.update_user, name='update_user'),
    path('delete_user/<str:pk>', views.delete_user, name='delete_user'),
    path('mainTableData/', views.mainTableData, name='mainTableData'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)