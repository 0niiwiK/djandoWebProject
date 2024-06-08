from django.contrib import admin
from django.urls import path, include
from carapp.views import login_view, search_view, download_images, register_view, add_car_view
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  ...
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search/', search_view, name='search'),
    path('download/<int:car_id>/', download_images, name='download_images'),
    path('add_car/', add_car_view, name='add_car'),  # URL para añadir coches
    path('api/', include('carapp.urls')),  # Incluye las URLs de la API
    path('', search_view, name='home'),  # URL para la página principal
]

