from rest_framework import serializers
from .models import Car, CarImage, CustomUser

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['image']

class CarSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )
    phone_number = serializers.CharField(write_only=True)
    uploaded_images = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['license_plate', 'phone_number', 'images', 'uploaded_images']

    def get_uploaded_images(self, obj):
        return CarImageSerializer(obj.images.all(), many=True).data

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        phone_number = validated_data.pop('phone_number')
        user = CustomUser.objects.get(phone_number=phone_number)

        license_plate = validated_data.get('license_plate')

        # Filtrar coches por la matrícula
        cars = Car.objects.filter(license_plate=license_plate)

        if cars.exists():
            # Si ya existe, actualizar el primero encontrado
            car = cars.first()
            car.uploaded_by = user
            car.save()

            # Eliminar imágenes existentes y agregar nuevas
            car.images.all().delete()
            for image_data in images_data:
                CarImage.objects.create(car=car, image=image_data)
        else:
            # Si no existe, crear uno nuevo
            car = Car.objects.create(uploaded_by=user, **validated_data)
            for image_data in images_data:
                CarImage.objects.create(car=car, image=image_data)

        return car
