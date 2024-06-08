import io
import os
import zipfile

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import CustomAuthenticationForm
from .models import Car
from .serializers import CarSerializer


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('search')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'carapp/login.html', {'form': form})

@login_required
def search_view(request):
    query = request.GET.get('q')
    if query:
        car = Car.objects.filter(license_plate=query).first()
        return render(request, 'carapp/car_detail.html', {'car': car})
    return render(request, 'carapp/search.html')

@login_required
def download_images(request, car_id):
    car = Car.objects.get(id=car_id)
    images = car.images

    # Crear un archivo zip en memoria
    zip_filename = f"{car.license_plate}_images.zip"
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for image in images:
            image_path = os.path.join(settings.MEDIA_ROOT, image)
            zip_file.write(image_path, os.path.basename(image_path))

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename={zip_filename}'
    return response


@api_view(['POST'])
def add_car_api(request):
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)