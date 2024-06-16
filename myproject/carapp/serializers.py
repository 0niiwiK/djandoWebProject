from rest_framework import serializers
from .models import Car, CarImage, CustomUser

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['image']

class CarSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False)
    )
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = Car
        fields = ['license_plate', 'phone_number', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        phone_number = validated_data.pop('phone_number')
        user = CustomUser.objects.get(phone_number=phone_number)
        car = Car.objects.create(uploaded_by=user, **validated_data)
        for image_data in images_data:
            CarImage.objects.create(car=car, image=image_data)
        return car