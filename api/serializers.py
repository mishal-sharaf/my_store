from rest_framework import serializers
from api.models import Products,Cart,Reviews
from django.contrib.auth.models import User


class ProductSeriealizers(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    name=serializers.CharField()
    price=serializers.IntegerField()
    description=serializers.CharField()
    category=serializers.CharField()
    image=serializers.ImageField()

class ProductModelSeriealizers(serializers.ModelSerializer):
    avg_rating=serializers.CharField(read_only=True)
    class Meta:
        model=Products
        fields="__all__"

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password"]

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class CartsSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    products=serializers.CharField(read_only=True)
    date=serializers.DateTimeField(read_only=True)
    class Meta:
        model=Cart
        fields="__all__"

class ReviewSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    product=serializers.CharField(read_only=True)
    class Meta:
        model=Reviews
        fields="__all__"