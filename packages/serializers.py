from rest_framework import serializers
from .models import PackageCategory, Package

class PackageCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageCategory
        fields = ['id', 'name']

class PackageSerializer(serializers.ModelSerializer):
    category = PackageCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=PackageCategory.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Package
        fields = [
            'id', 'name', 'description', 'price', 'duration',
            'departure_date', 'available_seats', 'is_active',
            'category', 'category_id'
        ]

