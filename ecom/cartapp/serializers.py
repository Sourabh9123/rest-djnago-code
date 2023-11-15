from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from cartapp.models import Cart, Cartitems, Order, Orderitem, Address, Transaction
from storeapp.models import Product
from storeapp.serializers import SimpleProductSerializer
from storeapp.serializers import ProductSerializer






# create cartitem serializer and update
class NewcartitemSerializer(ModelSerializer):
    
    class Meta:
        model = Cartitems
        fields = ['quantity', 'id','cart','product']
         



#get cartitem seralizer
class GetCartitemSerializer(ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Cartitems
        fields = ['id','quantity', 'product']
        depth = 1




class CartSerilizer(ModelSerializer):
   
    class Meta:
        model = Cart
        # fields = ['owner', 'id', 'cartitem', 'find_cart_total']
        fields = ['owner', 'id']








class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = ['name', 'user', 'address', 'id','state' ,'pincode','mobile',]


class OrderItemSerializer(ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Orderitem
        fields = ['order', 'product', 'quantity']








class OrderSerializer(ModelSerializer):
    order = OrderItemSerializer(read_only=True, many=True)
    # order_date = serializers.DateTimeField(format="%d %B %Y %I:%M %p")
    class Meta:
        model = Order
        fields = ['address','payment_status','owner', 'id','order',"order_payment_id","isPaid","amount"]
        # depth = 2 
        


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["payment_id","order_id","signature", "amount"]




















    #cartitem = serializers.SerializerMethodField( method_name= 'get_user_cartitems',read_only=True)
    # find_cart_total = serializers.SerializerMethodField(method_name='get_find_cart_total',read_only=True)
    
    # def get_user_cartitems(self, obj):
    #     cartitems = Cartitems.objects.filter(cart=obj)
    #     cartitem = NewcartitemSerializer(cartitems, many=True)
       
    #     return cartitem.data
    
    


    # def get_find_cart_total(self,obj):
    #     cartitems = Cartitems.objects.filter(cart=obj)
    #     total = sum([i.product.price * i.quantity for i in cartitems])
    #     return total
        










# #get one
# class CartItemsSerializer(ModelSerializer):
#     # product = serializers.UUIDField()
#     # cart = serializers.UUIDField()
#     total = serializers.SerializerMethodField(method_name="get_total")
#     class Meta:
#         model = Cartitems
#         # fields = ['cart', 'product','quantity','total', ]
#         fields = ['quantity','total']

#         depth = 1


#     def get_total(self,obj):
#         total_amount = 0
#         total_amount += obj.product.price * obj.quantity
#         return total_amount
    

#     def save(self,  **kwargs):
#         cart_id = self.context.get('cart_id')
#         product_id = self.context.get('product_id')
#         quantity = self.validated_data['quantity']
#         cart_instance = Cart.objects.get(id=cart_id)
#         product_instance = Product.objects.get(id=product_id)

#         try:
#             item_ = Cartitems.objects.filter(
#                 product_id=product_id)
#             if item_:
#                 print(item_,'------------')

#             cartitem = Cartitems.objects.get(
#                 cart=cart_instance,
#                 product = product_instance,
#             )
#             cartitem.quantity += quantity
#             cartitem.save()
#             self.instance = cartitem

#         except:
#             self.instance = Cartitems.objects.create(
#                 cart=cart_instance,
#                 product = product_instance,
#                 quantity = quantity 
#             )
#         return self.instance
    
    


#     def create(self, validated_data):
#         cart_id = self.context.get('cart_id')
#         product_id = self.context.get('product_id')
#         cart_instance = Cart.objects.get(id=cart_id)
#         product_instance = Product.objects.get(id=product_id)
#         import pdb
#         pdb.set_trace()
#         if cart_id:
#             cart_item_qs = Cartitems.objects.filter(
#                 id = cart_id
#             )
#             cart_item_qs.update(
#                 quantity = 1
#             )
#             return cart_item_qs.first()
#         else:
#             # Create a new Category instance
#             category_instance = Cartitems.objects.create(
#                 cart=cart_instance,
#                 product=product_instance,
#                 **validated_data
#             )


#         return category_instance






# class CartItemsListSerializer(ModelSerializer):
#     product = SimpleProductSerializer(many=False)
#     cart = serializers.UUIDField()
#     total = serializers.SerializerMethodField(method_name="get_total", read_only=True)
    
#     class Meta:
#         model = Cartitems
#         fields = ['id','cart', 'product','quantity','total']
#         depth = 1
    
    
#     def get_total(self,obj):
#         total_amount = 0
#         total_amount += obj.product.price * obj.quantity
#         return total_amount









# class CartSerializer(ModelSerializer):
#     # cart_total = serializers.SerializerMethodField(method_name="get_cart_total", read_only=True)
#     cart_user = CartItemsListSerializer(many=True)
#     total_cart = serializers.SerializerMethodField(method_name='get_grand_total',read_only=True)


#     class Meta:
#         model = Cart
#         fields = ['owner', 'id','cart_user','total_cart' ]
#         depth =1

#     def get_grand_total(self, obj):
#         items = obj.cart_user.all()
#         total_cart = sum([item.quantity * item.product.price for item in items])
  
#         return total_cart


