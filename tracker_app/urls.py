from django.urls import path
from .import views

urlpatterns = [
    path('',views.home),
    path('home.html',views.home),
    path('index.html',views.home2),
    path('inx.html',views.display),
    path('reg',views.registration),
    path('log',views.login_acc),
    path('wal',views.wallet_add),
    path('wal',views.display),
    path('log_out',views.logout)
   ]
