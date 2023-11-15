from django.contrib import admin
from cartapp.models import Address , Order, Orderitem, Transaction


admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Orderitem)



class TransactionAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'order_id', 'signature', 'amount', 'create_at']
    ordering = ['-create_at', 'payment_id']

admin.site.register(Transaction, TransactionAdmin)