from django.contrib.auth.decorators import login_required  # Decorador para requerir que el usuario esté autenticado
from django.shortcuts import redirect, render  # Para redirigir y renderizar vistas
from django.utils.decorators import method_decorator  # Decoradores para vistas basadas en clases
from django.views.decorators.csrf import csrf_exempt  # Decorador para eximir una vista de la verificación CSRF
from django.views.generic import FormView  # Vista genérica basada en clases para formularios
from rest_framework.parsers import MultiPartParser, FormParser  # Parsers para manejar datos multipart y form

from .forms import SearchForm  # Importar el formulario de búsqueda
from .models import Car  # Importar el modelo Car


@method_decorator(login_required, name='dispatch')  # Requiere que el usuario esté autenticado para acceder a esta vista
class CarSearchView(FormView):
    template_name = 'carapp/search.html'  # Plantilla a utilizar para la vista
    form_class = SearchForm  # Formulario a utilizar en la vista

    def form_valid(self, form):
        license_plate = form.cleaned_data['license_plate']  # Obtener la matrícula del formulario
        if license_plate:
            cars = Car.objects.filter(license_plate__icontains=license_plate)  # Buscar coches por matrícula
        else:
            cars = Car.objects.all()  # Obtener todos los coches

        if not cars.exists():
            return self.render_to_response(self.get_context_data(form=form, cars=[]))  # Si no hay coches, renderizar la plantilla con un contexto vacío
        elif cars.count() == 1:
            car = cars.first()  # Si hay un coche, redirigir a la vista de detalle del coche
            return redirect('car_detail', car_id=car.id)
        return self.render_to_response(self.get_context_data(form=form, cars=cars))  # Renderizar la plantilla con los coches encontrados

    def get(self, request, *args, **kwargs):
        form = self.get_form()  # Obtener el formulario
        return self.render_to_response(self.get_context_data(form=form))  # Renderizar la plantilla con el formulario


def car_not_found(request):
    return render(request, 'carapp/car_not_found.html')  # Renderizar la plantilla para coche no encontrado


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)  # Obtener el coche o lanzar un 404 si no existe
    return render(request, 'carapp/car_detail.html', {'car': car})  # Renderizar la plantilla de detalle del coche con el coche en el contexto


from django.contrib.auth.views import LoginView  # Vista genérica de Django para el login


class CustomLoginView(LoginView):
    template_name = 'carapp/login.html'  # Plantilla personalizada para la vista de login


from rest_framework.decorators import api_view, parser_classes  # Decoradores para vistas de la API
from rest_framework.response import Response  # Para devolver respuestas desde vistas de la API
from rest_framework import status  # Para utilizar códigos de estado HTTP
from .serializers import CarSerializer  # Importar el serializador para Car


@csrf_exempt  # Eximir esta vista de la verificación CSRF
@api_view(['POST'])  # Definir que esta vista solo acepta solicitudes POST
@parser_classes([MultiPartParser, FormParser])  # Definir los parsers para esta vista
def add_car_api(request):
    serializer = CarSerializer(data=request.data)  # Serializar los datos de la solicitud
    if serializer.is_valid():
        serializer.save()  # Guardar los datos si el serializador es válido
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Devolver los datos guardados y un estado 201
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Devolver los errores y un estado 400


from django.http import HttpResponse  # Para devolver respuestas HTTP
from django.shortcuts import get_object_or_404  # Para obtener un objeto o lanzar un 404 si no existe
import zipfile  # Para manejar archivos ZIP
import os  # Para manejar operaciones del sistema
from io import BytesIO  # Para manejar flujos de datos en memoria


def download_images(request, car_id):
    car = get_object_or_404(Car, id=car_id)  # Obtener el coche o lanzar un 404 si no existe
    images = car.images.all()  # Obtener todas las imágenes del coche

    zip_buffer = BytesIO()  # Crear un buffer en memoria para el archivo ZIP
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for image in images:
            if os.path.exists(image.image.path):  # Verificar si la imagen existe en el sistema de archivos
                zip_file.write(image.image.path, os.path.basename(image.image.path))  # Agregar la imagen al archivo ZIP

    zip_buffer.seek(0)  # Mover el puntero al inicio del buffer
    response = HttpResponse(zip_buffer, content_type="application/zip")  # Crear una respuesta HTTP con el contenido ZIP
    response['Content-Disposition'] = f'attachment; filename={car.license_plate}_images.zip'  # Definir el nombre del archivo adjunto
    return response  # Devolver la respuesta
