from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics
from cartapp.models import  Cartitems, Cart , Address, Order , Orderitem, Transaction
from storeapp.models import Product
from django.db import transaction
# from cartapp.serializers import CartItemsListSerializer, CartItemsSerializer, CartSerializer, NewcartitemSerializer
from rest_framework.response import Response
from cartapp.serializers import ( NewcartitemSerializer, CartSerilizer,
                                  SimpleProductSerializer, GetCartitemSerializer
                                  ,AddressSerializer, OrderSerializer, OrderItemSerializer,
                                  TransactionSerializer
                                 
)
from rest_framework import status
from storeapp.serializers import ProductSerializer 

from rest_framework.views import APIView
import razorpay


# PUBLIC_KEY = "rzp_test_b6Q27ppeBNZtMJ"
# SECRET_KEY = "gLCNbZNqQes9bX74Db4Wn19u"



PUBLIC_KEY = "rzp_test_DqyEDw9vF6Y4kA",

SECRET_KEY ="uibpbafCZAypJUX226PdWxBs"





# def create_order(amount, currency):
#     client = razorpay.Client(auth=("rzp_test_DqyEDw9vF6Y4kA", "uibpbafCZAypJUX226PdWxBs"))
#     response = client.order.create(
#         {
#         'amount': amount,
#         'currency': currency,
#         'payment_capture': 1  # Automatically capture payments
#     }
#     )
#     return response


# def capture_payment(order_id, payment_id):
#     client = razorpay.Client(auth=(PUBLIC_KEY, SECRET_KEY))
#     client.payment.capture(payment_id, order_id)







#adding item to cart and updating and delete item
class CartItemview(generics.GenericAPIView):

    def post(self,  request, *args, **kwargs):
        data = request.data
        id = kwargs.get('product_id')
        cart_ins = Cart.objects.get(owner=request.user)
        product_exist = Cartitems.objects.filter(product=id, cart=cart_ins.id).exists()
        if product_exist:
            product = Cartitems.objects.filter(product=id, cart=cart_ins.id).first()

            product_quantity = get_object_or_404(Product,id=id)

            if product_quantity.product_quantity >= request.data.get('quantity'):
               
                if product is not None:
                    
                    quantity = request.data.get('quantity')
                    new_qwn = quantity + product.quantity
                    product.quantity = new_qwn
                    product.save()
                    serializer = NewcartitemSerializer(product, many=False)
                    return Response(serializer.data, status=status.HTTP_200_OK)
    
        # this create new cartitem
        product = Product.objects.get(id=id)
        cart_ins = Cart.objects.get(owner=request.user)
        data['cart'] = cart_ins.id
        data['product'] = product.id


        serializer = NewcartitemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,  status=status.HTTP_200_OK)

            return Response( status=status.HTTP_400_BAD_REQUEST)
 
        return Response({"error":"error"},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,  request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        cart_ins = Cart.objects.get(owner=request.user)
        carttiem = Cartitems.objects.filter(cart= cart_ins  , product=product_id)
        carttiem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        

        





# cartitems view and total
class CartView(generics.GenericAPIView):


    def get(self, request, *args, **kwargs):
        cart_owner = request.user.id
        objs = Cart.objects.filter(owner=cart_owner)
      
        serializer = CartSerilizer(objs, many=True)
 
        user_cart_items = Cartitems.objects.filter(cart=objs[0])

        cartitems_serializer = GetCartitemSerializer(user_cart_items, many=True)
       
        cart_total = sum([i.quantity * i.product.price for i in user_cart_items]) 
     
        response_data = {
            **serializer.data[0],
            'cart_total' :cart_total,
            'cart_item' : cartitems_serializer.data,
        }

       
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(response_data, status=status.HTTP_200_OK)
    


class AddressView(generics.GenericAPIView):
    

    def post(self,  request, *args, **kwargs):
        data=request.data
        data['user'] = request.user.id
        serializer = AddressSerializer(data=data)
        print(data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,  request, *args, **kwargs):

        objs = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class PlaceOrderView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        
        order = Order.objects.filter(owner=user.id).first()
        print(order)
        if order is not None:
            serializers = OrderSerializer(order, many=True)

            orderitems = Orderitem.objects.filter(order=order)
            orderitems_serializer = OrderItemSerializer(orderitems, many=True)
        
            

            response_data = {
                **serializers.data[0],
                'orderitem' : orderitems_serializer.data,

            }
        else:
            response_data = {
                
                    'orderitem' : "No item in cart"

                }
     
        return Response(response_data, status=status.HTTP_200_OK) 


    def post(self, request, *args, **kwargs):
        print('outer side')

        try:


            user_id = request.user.id

            total_cartitems = Cartitems.objects.filter(cart__owner__id = user_id)
            total_price = sum([i.quantity * i.product.price for i in total_cartitems])

            print('inner body')



            # order_data = create_order(total_price, "INR")
    
            client = razorpay.Client(auth=("rzp_test_DqyEDw9vF6Y4kA", "uibpbafCZAypJUX226PdWxBs"))

            data = { "amount": int(total_price) *100, "currency": "INR", "receipt": "order_rcptid_11" ,"payment_capture": "1",}
            payment = client.order.create(data=data)

            print(payment)
        
            user=request.user

            cartitems = Cartitems.objects.filter(cart__owner=user)

            print('after cartitems')
            

            address = Address.objects.get(user=user.id)
            

            ########### patment logic after payment this will run 
        
            with transaction.atomic():        
                order = Order.objects.create(address=address, payment_status='P',owner= user, amount=total_price, order_payment_id = payment['id']) 
                orderitem =  [  Orderitem(order=order, product=item.product, quantity=item.quantity)    for item in cartitems ]
                Orderitem.objects.bulk_create(orderitem)
            
                # order_payment_id=payment.get('id')

                for i in cartitems:
                    product = i.product
                    if product.product_quantity >= i.quantity:
                        product.product_quantity -= i.quantity
                    else:
                        return Response({"error":"error not sufficent quantity"} ,status=status.HTTP_400_BAD_REQUEST)

                    product.save()    
                cartitems.delete()

                serializer = OrderSerializer(order)
                data = {
                    "payment": payment,
                    "order": serializer.data,
                    
                }
                return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            
            return Response({'done':'Something went wrong try again',"error":str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                
        return Response({'done':'done', }, status=status.HTTP_200_OK)





class TransactionView(generics.GenericAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction

    def post(self, request, *args, **kwargs):
        serialzier = TransactionSerializer(data=request.data)
        print(request.data)
        if serialzier.is_valid():
        

            try:
                razorpay_order_id =  serialzier.validated_data.get('order_id')
                razorpay_payment_id = serialzier.validated_data.get('payment_id')
                razorpay_signature = serialzier.validated_data.get('signature')

                client = razorpay.Client(auth=("rzp_test_DqyEDw9vF6Y4kA", "uibpbafCZAypJUX226PdWxBs"))         
                client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
                })

                try:
                    order = Order.objects.get(order_payment_id = razorpay_order_id)
                
                    order.isPaid = True
                    order.payment_status = "C"
                    order.save()
                except  Exception as e:
                    pass

            except Exception as e :
                return Response({"error":str(e), "payment":"payment not verify"})
            serialzier.save()
            return Response(serialzier.data, status=status.HTTP_201_CREATED)
        return Response( serialzier.errors,status=status.HTTP_400_BAD_REQUEST)




















































# class CartItemsView(generics.ListCreateAPIView, generics.UpdateAPIView):
    
#     def get_queryset(self):
#         return Cartitems.objects.filter(cart=self.request.user.cart_owner_user.id)

#     # def get_queryset(self):
#     #     return Cartitems.objects.filter(cart=self.kwargs.get('uuid'))
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return CartItemsListSerializer
#         return CartItemsSerializer
    

#     def get_serializer_context(self):
#         cart_id =self.request.user.cart_owner_user.id
        
#         return {'product_id':self.kwargs.get('uuid'),'cart_id':cart_id}
    



    
# class CartItemsView(generics.GenericAPIView):
    

#     def get(self, request, *args, **kwargs):
#         cartitems = Cartitems.objects.filter(cart=request.user.cart_owner_user.id) 
#         serializer = CartSerializer(cartitems,  many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def update(self, request,  *args, **kwargs):
#         cartitems = Cartitems.objects.filter(cart=request.user.cart_owner_user.id) 
#         if property.id in cartitems:
#             print("yes")
    
    
#     def get_serializer_context(self):
#         cart_id =self.request.user.cart_owner_user.id
        
#         return {'product_id':self.kwargs.get('uuid'),'cart_id':cart_id}
    







# class CartView(APIView):
#     # serializer_class = CartSerializer
#     # # queryset = Cart.objects.all()

#     # def get_queryset(self):
#     #     pk = self.kwargs.get('cart_id')
#     #     return get_object_or_404(Cart,id=pk)
    
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('cart_id')
    
#         query_set = get_object_or_404(Cart, id=pk)
#         serializer = CartSerializer(query_set, many=False)

#         return Response(serializer.data,  status=status.HTTP_200_OK)
    
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('cart_id')
        
#         query_set = get_object_or_404(Cart, id=pk)
#         query_set.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)








# class CartItemViewSet(generics.ListAPIView):
    
#     serializer_class = CartItemsListSerializer

#     def get_queryset(self):
#         print(self.request.user.id)
#         cart_id =  self.kwargs.get('uuid')
#         return  Cartitems.objects.get(cart__owner__id=self.request.user.id)
    

 # return Response({"payment": payment})
        
        # data = None

        # client = razorpay.Client(auth=(PUBLIC_KEY, SECRET_KEY))
        # print(client,'--------------------')
        
        # payment  = {
        #         'amount': int(total_price) * 100,  # Amount in paise
        #         'currency': 'INR',
        #         "payment_capture": "1",
        #     }
        # payment = client.order.create(data=payment_data)
        
        
        

        """order response will be 
            {'id': 17, 
            'order_date': '23 January 2021 03:28 PM', 
            'order_product': '**product name from frontend**', 
            'order_amount': '**product amount from frontend**', 
            'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""
        # print(payment,'________________________________------------')
