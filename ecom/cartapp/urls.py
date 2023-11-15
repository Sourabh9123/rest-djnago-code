from django.urls import path
from cartapp.views import CartItemview, CartView, AddressView,PlaceOrderView, TransactionView



urlpatterns = [
    ###########
    path('addcart/<uuid:product_id>/',CartItemview.as_view(), name='cart_items' ), # create cartitem and update
    path('', CartView.as_view(),  name='cart'),  #view cartitems 
    path('address/', AddressView.as_view(), ),
    path('order/', PlaceOrderView.as_view(), ),
    path('order/transaction/', TransactionView.as_view(), ),



]



