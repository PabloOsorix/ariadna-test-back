from django.urls import path
from .views import NewCategoryView, ListCategoriesView, DeleteCategoryView
urlpatterns = [
    path('new-category', NewCategoryView.as_view()),
    path('categories', ListCategoriesView.as_view()),
    path('delete-category', DeleteCategoryView.as_view()),
]