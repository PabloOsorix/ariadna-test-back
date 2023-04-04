from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer
# Create your views here.


class ListCategoriesView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, form=None):
        try:
            categories = Category.objects.all()
            categories = CategorySerializer(categories, many=True)
            if len(categories.data) > 0:
                return Response(
                    {'categories': categories.data},
                    status=status.HTTP_200_OK
                )
        except Exception:
            return Response(
                {'error': Exception},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class NewCategoryView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, form=None):
        data = self.request.data

        try:
            name = str(data['name'])

            if name in [None, '']:
                return Response(
                    {'error': 'name is mandatory could not be empty'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'name is mandatory could not be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            description = data["description"]

            if description in [None, ""]:
                return Response(
                    {"error": "description is mandatory could not be empty"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'description is mandatory could not be empty'}
            )
        try:
            parent_id = data["parent_id"]
        except:
            parent_id = None
        
        if parent_id is not None and Category.objects.filter(id=parent_id).exists():
            parent_category = Category.objects.get(id=parent_id)
        else:
            parent_category = None

        new_category = Category(
            name=name, description=description, parent=parent_category)
        new_category.save()
        new_category = CategorySerializer(new_category)

        if len(new_category.data) > 0:
            return Response(
                {"new_category": new_category.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': 'problem with searializer'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteCategoryView(APIView):
    permission_classes = (permissions.AllowAny,)
    def delete(self, request, format=None):
        category_id = self.request.query_params.get('category_id')

        try:
            category_id = int(category_id)

        except:
            return Response(
                {'error': 'category_id is mandatory and must be an integer'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            if Category.objects.filter(id=category_id).exists():
                category = Category.objects.get(id=category_id)
                category.delete()
                return Response(
                    {'category delete successsfuly'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'category was not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except:
            return Response(
                {'error': 'category could not be delete'},
                status=status.HTTP_404_NOT_FOUND
            )
