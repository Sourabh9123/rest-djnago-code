from django.shortcuts import render
from rest_framework  import  generics
from storeapp.models import Product, Category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from storeapp.serializers import ( ProductSerializer, CategorySerializer )
from rest_framework.pagination import  PageNumberPagination
from rest_framework import pagination
from rest_framework.filters import SearchFilter






class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10









class CategoryDetailView(generics.GenericAPIView):

    def get_queryset(self):
        uuid = self.kwargs.get('category_uuid')
        if uuid:
            try:
                return get_object_or_404(Category, id=uuid)
            except:
                return Category.objects.none()
        return Category.objects.none()
    
    serializer_class = CategorySerializer



    def get(self,  request, *args, **kwargs):
        qs = self.get_queryset()
        if qs:
            serializer = self.get_serializer(qs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,  request, *args, **kwargs):
        data =  request.data
        qs = self.get_queryset()
        if qs:

            serializer = CategorySerializer(instance=qs, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request, *args, **kwargs):
        qs = self.get_queryset()
        if qs:
            qs.delete()
            return Response({"result_is":'No content'}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
            

    




class ProductDetailView(generics.GenericAPIView):
    def get_queryset(self):
        return  Product.objects.all()
    
    serializer_class = ProductSerializer


    

    def get(self,  request, *args, **kwargs):
        product_id = kwargs.get('product_uuid')
   
        qs = None
        try:
            qs = Product.objects.filter(id=product_id).first()
        
        except Product.DoesNotExist:
            return Response({"errors":' product Not exists'},  status=status.HTTP_404_BAD_REQUEST)

        except Exception as e :
            return Response({"errors":str(e)},  status=status.HTTP_404_BAD_REQUEST)
        
        else:        
            if qs is not None:
                serializer = self.get_serializer(qs)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response( {"error" :"not found "}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


    def put(self, request, *args, **kwargs):
        data = request.data
        product_instance = None
        try:
            uuid = kwargs.get('product_uuid')
      
            product_instance = Product.objects.filter(id=uuid).first()
        except Product.DoesNotExist:
            return Response({"errors" : "does not exists"},status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"errors" : str(e)},status=status.HTTP_400_BAD_REQUEST)
    
        if product_instance is not None:
            product_instance.name = data.get('name', product_instance.name)
            product_instance.discription = data.get('discription', product_instance.discription)
            category_instance =  Category.objects.filter(id=data.get('category', product_instance.category_id)).exists()
            # try except will come here
            if category_instance:
                product_instance.category_id = data.get('category', product_instance.category_id)
            else:
                return Response({"errors" : 'category is not correct'},status=status.HTTP_400_BAD_REQUEST)


            product_instance.price = data.get('price', product_instance.price)
            product_instance.product_quantity = data.get('product_quantity', product_instance.product_quantity)
            product_instance.avalible_sizes = data.get('avalible_sizes', product_instance.avalible_sizes)
            product_instance.save()
        
            serializer = ProductSerializer(product_instance, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"errors" : "not updated"},status=status.HTTP_400_BAD_REQUEST)
          

class ProductListCreateView(generics.GenericAPIView):

    def get_queryset(self):
        return Product.objects.all()
    
    
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name' ,  'price']
    
    
    def get(self, request, *args, **kwargs):

        products = self.filter_queryset(Product.objects.all()).order_by('-created_at')

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductSerializer(page, many=True , context={"request":request})
            return self.get_paginated_response(serializer.data)

        else:
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        """
        Createing Product Instance
        """
        
        try:
            new_data = {
                "name": request.data['name'],
                "discription": request.data['discription'],
                "category_id": request.data['category'] ,
             
                "price":  request.data['price'],
                "product_quantity":  request.data['product_quantity'],
                "avalible_sizes":  request.data['avalible_sizes'],
                "image" : request.data['image'],
            }
            product = Product.objects.create(**new_data)
            serializer = ProductSerializer(product,many=False)
            response ={
                "created": 1
            }
        except:
            response ={
                "created": 0
            }

            return Response(response,status=status.HTTP_400_BAD_REQUEST)

        return Response(response,status=status.HTTP_201_CREATED)



    


   

class CategoryCreateListView(generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get(self,  request, *args, **kwargs):

        category =  Category.objects.all()
        category_seralizer = CategorySerializer(category, many=True)

        return Response(category_seralizer.data, status=status.HTTP_200_OK)
     

    def post(self, request, *args, **kwargs):
      
       
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data, status=status.HTTP_200_OK)
        
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







       



# if qs:                          
    # new_data = {

        
    # "name": data.get('name', qs.name),
    
    # "discription": data.get('discription', qs.discription),
    # "category_id":  data.get('category', qs.category.id),
    # # "image":  data.get('image', qs.image),  # this need file that's why it comanted
    # "price":  data.get('price', qs.price),
    # "product_quantity":  data.get('product_quantity', qs.product_quantity),
    # "avalible_sizes":  data.get('avalible_sizes', qs.avalible_sizes), 
    # }


    # serializer = ProductSerializer(instance=qs, data=new_data, partial=True )
    # if serializer.is_valid():
    #     serializer.save()
    #     print('indse of serializer_____________________ valid')
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)












#  old_cat = data.get('category')
#             print(old_cat)
#             if old_cat:
#                 category_id = Category.objects.filter(id=old_cat).filter()







# category = Category.objects.all()[0]
# sub_category = SubCategory.objects.all()[0]
# print(category.id, sub_category.id)
# data = {
#     "name" : 'Red sweat shirt ',
#     "category_id" :    category.id,
#     "sub_category_id" : sub_category.id,
#     "price" : 999,
#     "discription" : "Yes create by validate nest",
#     "product_quantity" : 91,
#     "avalible_sizes" : "S",
# }


# print(data)

# # product_create = Product.objects.create(
# #     name= "Red sweat shirt",
# #     category_id = category.id,
# #     sub_category_id = sub_category.id,
# #     price = 299,
# #     discription = "discription after adding _id",
# #     product_quantity = 91,
# #     avalible_sizes = "S",
# # ) 
# # if product_create:
# #     print('done')

# product_create = Product.objects.create(**data) 