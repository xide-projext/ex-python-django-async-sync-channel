"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from django.http import JsonResponse

def my_view_sync(request):
    # 요청 처리 로직
    return JsonResponse({'message': '동기 처리 응답 메시지 : 항상 완료'})

def my_view_async(request):
    # 요청 처리 로직
    return JsonResponse({'message': '비동기 처리 응답 메시지 : 상태 시작했음'})


def my_view_async_status(request):
    # 요청 처리 로직
    return JsonResponse({'message': '비동기 처리 응답 메시지 : 상태 완료했음'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", cache_page(60 * 15)(TemplateView.as_view(template_name="home.html")), name="home"),
    path('path-to-your-backend-endpoint-sync', my_view_sync, name='my_view_sync'),
    path('path-to-your-backend-endpoint-async', my_view_async, name='my_view_async'),
    path('path-to-your-backend-endpoint-async-status', my_view_async_status, name='my_view_async_status'),
]
