from django.contrib import admin

from storeapp.models import Category, Product, ProductAttribute, ColorAttribute, SizeAttribute


from cartapp.models import Cart, Cartitems


class CartAdmin(admin.ModelAdmin):
    list_display = ['owner', 'id']

admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']


admin.site.register(Cartitems, CartItemAdmin)



admin.site.register(ProductAttribute)

admin.site.register(ColorAttribute)

admin.site.register(SizeAttribute)




class ProductAdmin(admin.ModelAdmin):
    list_display = ['name',"avalible_sizes",'product_quantity' ,"price",'discription','id','category',]

admin.site.register(Product,ProductAdmin )






class CategoryAdmin(admin.ModelAdmin):
 
    list_display = ['name', 'discription','id', ]
    

admin.site.register(Category, CategoryAdmin)

