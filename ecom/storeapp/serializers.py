from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.reverse import reverse
from storeapp.models import Category , Product, ProductAttribute,SizeAttribute,ColorAttribute










class ColorAttributeSerializer(ModelSerializer):
    class Meta:
        model = ColorAttribute
        fields = "__all__"



class SizeAttributeSerializer(ModelSerializer):
    class Meta:
        model = SizeAttribute
        fields = "__all__"



class ProductAttributeSerializer(ModelSerializer):
    size = SizeAttributeSerializer()
    color = ColorAttributeSerializer()
    class Meta:
        model = ProductAttribute
        fields = ['product','size',"color"]







class CategorySerializer(ModelSerializer):
    
  
    class Meta:
        model = Category
        fields = ['id', 'name', 'discription',]


    # def create(self, validated_data):
    #     sub_category_data = validated_data.pop('sub_category')
    #     sub_category_instance  = SubCategory.objects.create(**sub_category_data)

    #     category_instance = Category.objects.create(
    #             sub_category = sub_category_instance,
    #             **validated_data
    #     )

    #     return category_instance

    

    


class ProductSerializer(ModelSerializer):
    category = CategorySerializer()
    category_detail = serializers.SerializerMethodField(read_only=True)
    product_attribute = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = ["product_attribute",'id','name',"category_detail", 'discription',  
                  'category',"image", 'price',  'product_quantity', 'avalible_sizes']
        depth = 1

       
    def get_product_attribute(self, obj):
        try:
            product_attributes = ProductAttribute.objects.filter(product=obj.id)
            serializer = ProductAttributeSerializer(product_attributes, many=True)
            return serializer.data
        except Exception as e:
            return None


    def get_category_detail(self, obj):
 
        request = self.context.get('request')
        # return f"/api/store/product/{obj.id}/"
        if request is None:
           return None
        return  reverse("category-detail", kwargs={"category_uuid":obj.category.id}, request=request)

    

    # category = CategorySerializer(source='category_products', read_only=True)
    # sub_category = SubCategorySerializer(source='sub_category_subcategories', read_only=True)

    
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # sub_category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())
    
    # category_url = serializers.HyperlinkedIdentityField(
    #     view_name='product-detail',
    #     lookup_field = 'id'
    #     )
       
    # def get_cart_total(self, obj):
    #     total = 0
    #     if  obj.total is not None:
    #         total += obj.total
    #         return total



    

class SimpleProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', "price"]

