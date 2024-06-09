from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from carapp.views import CustomLoginView, CarSearchView, download_images, add_car_api, car_not_found, car_detail

from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  ...
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('search/', CarSearchView.as_view(), name='search'),
    path('download/<int:car_id>/', download_images, name='download_images'),
    path('api/add_car/', add_car_api, name='add_car_api'),
    path('car_not_found/', car_not_found, name='car_not_found'),
    path('car/<int:car_id>/', car_detail, name='car_detail'),  # URL para detalles del coche
    path('', CarSearchView.as_view(), name='home'),  # Página principal y de búsqueda combinada
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
