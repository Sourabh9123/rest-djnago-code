from django.urls import path
from storeapp.views import(
     ProductListCreateView, CategoryCreateListView, 
     ProductDetailView, CategoryDetailView

)


urlpatterns = [
    path('product/', ProductListCreateView.as_view(), name='product'),
    path('product/<uuid:product_uuid>/', ProductDetailView.as_view(), name='product-detail'),
    path('category/', CategoryCreateListView.as_view(), name='category'),
    path('category/<uuid:category_uuid>/', CategoryDetailView.as_view(), name='category-detail'),
]
