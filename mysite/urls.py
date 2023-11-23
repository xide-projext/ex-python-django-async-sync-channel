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
import asyncio
import asyncio.subprocess as subprocess
import uuid

# async는 없어도 되지만 2초 걸리는 가짜 작업을 실행하기 위해서
async def my_view_sync(request):
    # 요청 처리 로직
    # await asyncio.sleep(5)

    # 'sleep 10' 명령어 실행
    process = await subprocess.create_subprocess_shell(
        'sleep 3 && ls -al',
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    print(f'sleep 3 && ls -al exited with {process.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

    # 프로세스가 완료되면 메시지 출력
    print("프로세스 완료!")
    return JsonResponse({'message': '동기 처리 응답 메시지 : 항상 완료 : 3초 걸렸음'})



processes = {}


async def my_view_async(request):
    # 요청 처리 로직
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    unique_id = str(uuid.uuid4())
    process = loop.run_until_complete(
        asyncio.create_subprocess_shell(
            'sleep 10 && ls -al',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
    )

    processes[unique_id] = process
    loop.close()
    return JsonResponse({'message': f'비동기 처리 응답 메시지 : 상태 시작했음 \n unique_id: {unique_id}'})


def my_view_async_status(request, unique_id):
    process = processes.get(unique_id)

    if process is None:
        return JsonResponse({'status': 'unknown', 'message': '프로세스 ID가 존재하지 않음'})

    if process.returncode is None:
        status = 'running'
    else:
        status = 'completed' if process.returncode == 0 else 'error'

    return JsonResponse({'status': status, 'return_code': process.returncode})


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", cache_page(60 * 15)(TemplateView.as_view(template_name="home.html")), name="home"),
    path('path-to-your-backend-endpoint-sync', my_view_sync, name='my_view_sync'),
    path('path-to-your-backend-endpoint-async', my_view_async, name='my_view_async'),
    path('path-to-your-backend-endpoint-async-status/<str:unique_id>/', my_view_async_status, name='my_view_async_status'),
]
