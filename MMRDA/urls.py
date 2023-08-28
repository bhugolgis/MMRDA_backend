
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , include 
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="MMRDA API",
      default_version='v1',
      description="description of MMRDA project",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/auth/' ,include('Auth.urls') ),
    path('api/envmonitoring/' , include('EnvMonitoring.urls')),
    path('api/socialmonitoring/' , include('SocialMonitoring.urls')),
    path('api/traning/' , include('Training.urls')),
    path('api/report/' , include('Report.urls')),
    path('api/dashboard/' , include('Dashboard.urls')),
    path('api/GIS/' , include('GIS.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
