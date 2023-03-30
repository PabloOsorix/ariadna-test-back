from django.urls import path
from .views import NewProductView, ProductDetailView, ListProductByCategory, UpdateProductView, DeleteProductView


urlpatterns = [
    path('new-product', NewProductView.as_view()),
    path('product/<product_id>', ProductDetailView.as_view()),
    path('search-by-category', ListProductByCategory.as_view()),
    path('update-product', UpdateProductView.as_view()),
    path('delete-product', DeleteProductView.as_view())
]