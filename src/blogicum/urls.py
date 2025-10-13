"""blogicum URL Configuration

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
from django.contrib.auth.forms import UserCreationForm
from django.urls import path, include, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

import psutil

def simple_metrics(request):
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    metrics = f"""
# HELP memory_available_bytes Available memory
# TYPE memory_available_bytes gauge
memory_available_bytes {memory.available}

# HELP memory_used_bytes Used memory  
# TYPE memory_used_bytes gauge
memory_used_bytes {memory.used}

# HELP disk_free_bytes Free disk space
# TYPE disk_free_bytes gauge
disk_free_bytes {disk.free}

# HELP http_requests_total HTTP requests count
# TYPE http_requests_total counter
http_requests_total{{endpoint="/metrics"}} 1

# HELP application_working Application status
# TYPE application_working gauge
application_working 1
"""
    return HttpResponse(metrics, content_type='text/plain')

urlpatterns = [
    path('prometheus-metrics', simple_metrics),
    path('', include('blog.urls', namespace='blog')),
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'pages.views.permission_denied'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
