from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..categories.models import Category
from .models import Product
from .serializers import ProductSerializer
# Create your views here.


class NewProductView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        """
        Http post method to create a new product,
        required parameters:
        (name): string
        (category): string
        (price): float
        (value): float
        (stock): int

        """
        data = self.request.data

        try:
            name = data['name']
            if name in [None, '']:
                return Response(
                    {'error': 'parametrer name is mandatory and may not be empty'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'parameter name is mandatory'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            category = data['category']

            if category not in [None, ''] and Category.objects.filter(id=category).exists():
                category = Category.objects.get(id=category)
            else:
                return Response(
                    {'error': 'category not found, check parameter'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except:
            return Response(
                {'error': 'parameter category is mandatory could not be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            price = float(data['price'])

            if isinstance(price, float) == False:
                return Response(
                    {'error': 'price must be float, (decimal)'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'parameter price is mandatory could not be empty or integer'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            value = float(data['value'])

            if isinstance(value, float) == False:
                return Response(
                    {'error': 'parameter value must be float, (decimal)'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'parameter value is mandatory, could not be empty or integer'}
            )

        try:
            stock = int(data['stock'])

            if isinstance(stock, int) == False:
                return Response(
                    {'error': 'parameter value must be integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'parameter stock is mandatory, could not be empty or decimal'},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_product = Product(
            name=name,
            category=category,
            price=price,
            value=value,
            stock=stock,
        )

        new_product.save()
        new_product_searialized = ProductSerializer(new_product)
        if len(new_product_searialized.data) > 0:
            return Response(
                {'new_product': new_product_searialized.data},
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                {'error': 'error trying to serialize data'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductDetailView(APIView):
    def get(self, request, product_id, format=None):

        try:
            product_id = int(product_id)

        except:
            return Response(
                {'error': 'product id must be an integer'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Product.objects.filter(id=product_id).exists():
            product = Product.objects.get(id=product_id)
            product = ProductSerializer(product)

            return Response(
                {'product': product.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'product with this ID does not exists'},
                status=status.HTTP_404_NOT_FOUND
            )


class ListProductByCategory(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data
        sort_by = 'date_created'

        try:
            category_id = int(data['category_id'])
        except:
            return Response(
                {'error': 'category ID must be an integer'},
                status=status.HTTP_404_NOT_FOUND
            )

        if category_id == 0:
            product_result = Product.objects.all()

        elif not Category.objects.filter(id=category_id).exists():
            return Response(
                {'error': 'This category does not exists'},
                status=status.HTTP_404_NOT_FOUND
            )

        else:

            category = Category.objects.get(id=category_id)
            if category.parent:
                """if category has a parent just return current category
                and ignore parent category"""
                product_result = Product.objects.filter(category=category)

            else:

                if not Category.objects.filter(parent=category).exists():
                    """if category hasn't children return return objects in
                    the current category"""
                    product_result = Product.objects.filter(category=category)

                else:
                    """Return all children of the category"""

                categories = Category.objects.filter(parent=category)
                filtered_categories = [category]

                for cat in categories:
                    filtered_categories.append(cat)

                filtered_categories = tuple(filtered_categories)
                product_result = Product.objects.filter(
                    category__in=filtered_categories)

        product_result = product_result.order_by(sort_by)
        product_result = ProductSerializer(product_result, many=True)

        if len(product_result.data) > 0:
            return Response(
                {'products_by_category': product_result.data},
                status=status.HTTP_200_OK
            )


class UpdateProductView(APIView):
    def put(self, request, format=None):
        data = self.request.data
        try:
            product_id = int(data['product_id'])

            if isinstance(product_id, int) == False:
                return Response(
                    {'error': 'product id must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'product id must be an integer'},
                status=status.HTTP_400_BAD_REQUEST
            )

        check = check_data_update(data)
        if isinstance(check, Response):
            return check
        print(data)
        product_to_update = Product.objects.get(id=product_id)
        del data['product_id']
        updated_product = ProductSerializer(
            product_to_update, data=data, partial=True)
        

        if updated_product.is_valid():
            updated_product.save()
            return Response(
                {'updated_product': updated_product.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'error in updating proccess'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteProductView(APIView):
    def delete(self, request, format=None):

        product_id = self.request.query_params.get('product_id')

        try:
            product_id = int(product_id)
        except:
            return Response(
                {'error': 'product_id is mandatory, it must be an integer'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if Product.objects.filter(id=product_id).exists():
            product_to_delete = Product.objects.get(id=product_id)
            product_to_delete.delete()
            return Response(
                {'success': 'product was deleted successfully'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Product was not found'},
                status=status.HTTP_404_NOT_FOUND
            )


def check_data_update(data: dict) -> bool | Response:
    try:
        if data['name'] in [None, '']:
            del data['name']
        else:
            data['name'] = str(data['name'])
    except:
        pass
    try:
        if data['category_id'] in [None, '']:
            del data['category_id']

        elif data['category_id']:
            data['category_id'] = int(data['category_id'])


            if isinstance(data['category_id'], int) == False:
                return Response(
                    {'error': 'parameter category is mandatory could not be empty, it must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            else:
                if not Category.objects.filter(id=data['category_id']).exists():
                    return Response(
                        {'error': 'Category not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                else:
                    data['category_id'] = Category.objects.get(
                        id=data['category_id'])
    except:
        pass

    try:
        if data['price'] in [None, ""]:
            del data['price']

        else:
            data['price'] = float(data['price'], 6)
            if isinstance(data['price'], float) == False:
                return Response(
                    {'error': 'price must be float, (decimal)'},
                    status=status.HTTP_400_BAD_REQUEST
                )
    except:
        pass
    
    try:
        if data['value'] in [None, ""]:
            del data['value']

        else:
            data['value'] = float(data['value'], 6)
            if isinstance(data['value'], float) == False:
                return Response(
                    {'error': 'value must be float, (decimal)'},
                    status=status.HTTP_400_BAD_REQUEST
                )
    except:
        pass
        
    try:
        if data['stock'] in [None, ""]:
            del data['stock']

        else:
            data['stock'] = int(data['stock'])
            if isinstance(data['stock'], int) == False:
                return Response(
                    {'error': 'stock must be an integer.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
    except:
        pass

    return True
