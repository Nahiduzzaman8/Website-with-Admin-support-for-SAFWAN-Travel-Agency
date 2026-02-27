from django.contrib import admin
from .models import Package, PackageCategory

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name','category','price','departure_date', 'available_seats', 'is_active')

@admin.register(PackageCategory)
class PackageCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)