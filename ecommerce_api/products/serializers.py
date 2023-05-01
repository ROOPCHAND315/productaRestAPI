from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def create(self,validated_data):
        return Product.objects.create(**validated_data) 
    

    def update(self,instance,validated_data):
        #instance mean jo purana data h DB me
        instance.name=validated_data.get('name',instance.name)
        print(instance.name)
        instance.description=validated_data.get('description',instance.description)
        instance.price=validated_data.get('price',instance.price)
        instance.save()
        return instance