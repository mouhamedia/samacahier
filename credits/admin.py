from django.contrib import admin
from .models import Credit, Payment


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ('client', 'boutiquier', 'amount', 'paid_amount', 'status', 'due_date', 'created_at')
    list_filter = ('status', 'boutiquier', 'created_at')
    search_fields = ('client__name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('credit', 'amount', 'payment_date', 'payment_method', 'created_at')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('credit__client__name',)
    readonly_fields = ('created_at', 'payment_date')   
