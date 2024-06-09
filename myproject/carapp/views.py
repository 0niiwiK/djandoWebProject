from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
import logging

from django.utils.decorators import method_decorator
from django.views.generic import FormView

from .forms import SearchForm
from .models import Car


@method_decorator(login_required, name='dispatch')
class CarSearchView(FormView):
    template_name = 'carapp/search.html'
    form_class = SearchForm

    def form_valid(self, form):
        license_plate = form.cleaned_data['license_plate']
        if license_plate:
            cars = Car.objects.filter(license_plate__icontains=license_plate)
        else:
            cars = Car.objects.all()

        if not cars.exists():
            return self.render_to_response(self.get_context_data(form=form, cars=[]))
        elif cars.count() == 1:
            car = cars.first()
            return redirect('car_detail', car_id=car.id)
        return self.render_to_response(self.get_context_data(form=form, cars=cars))

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))


def car_not_found(request):
    return render(request, 'carapp/car_not_found.html')


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'carapp/car_detail.html', {'car': car})


from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'carapp/login.html'


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CarSerializer


@api_view(['POST'])
def add_car_api(request):
    serializer = CarSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import zipfile
import os
from io import BytesIO


def download_images(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    images = car.images.all()

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for image in images:
            if os.path.exists(image.image.path):
                zip_file.write(image.image.path, os.path.basename(image.image.path))

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type="application/zip")
    response['Content-Disposition'] = f'attachment; filename={car.license_plate}_images.zip'
    return response
