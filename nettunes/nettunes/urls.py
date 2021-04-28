"""nettunes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from catalog import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.catalog, name='catalog'),
    path('about/', views.about, name='about'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('user/<str:username>/', views.account, name='user'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    path('request-record/', views.request_record, name='request-record'),
    path('return-rental/', views.return_rental, name='return-rental'),
    path('move-up/', views.move_request_up, name='move-up'),
    path('cancel-request/', views.cancel_request, name='cancel-request'),
]
