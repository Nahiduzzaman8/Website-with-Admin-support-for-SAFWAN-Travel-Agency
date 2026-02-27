from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Package, PackageCategory
from .serializers import PackageSerializer, PackageCategorySerializer
from accounts.decorators import jwt_required

# List all active packages (public)
class PackageListView(APIView):
    def get(self, request):
        packages = Package.objects.filter(is_active=True)
        serializer = PackageSerializer(packages, many=True)
        return Response(serializer.data)

# Package Detail (public)
class PackageDetailView(APIView):
    def get(self, request, pk):
        try:
            package = Package.objects.get(id=pk, is_active=True)
        except Package.DoesNotExist:
            return Response({'error': 'Package not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PackageSerializer(package)
        return Response(serializer.data)

