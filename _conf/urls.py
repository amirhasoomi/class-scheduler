"""classScheduler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_yasg2 import openapi
from drf_yasg2.views import get_schema_view
from django.views.decorators.cache import never_cache
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
]

DRF_DESCRIPTION = ""

if settings.DRF_ENABLED:
    # from utils.views import postman

    schema_view = get_schema_view(
        openapi.Info(
            title="Stroke API",
            default_version='v1',
            description=DRF_DESCRIPTION,
        ),
        permission_classes=(permissions.AllowAny,),
        patterns=urlpatterns,
    )
    # noinspection PyUnresolvedReferences
    schema = schema_view.with_ui('swagger')

    urlpatterns += [
        path('swagger/', never_cache(schema)),
        # path('postman/<str:token>/', never_cache(postman(schema))),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
