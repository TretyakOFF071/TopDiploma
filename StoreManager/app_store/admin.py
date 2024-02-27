from django.contrib import admin
from .models import Profile, GoodCategory, Provider, Good, Supply, SaleItem, Sale


class GoodAdmin(admin.ModelAdmin):
    model = Good
    list_display = ['name', 'category', 'selling_price', 'purchase_price', 'description', 'image', 'quantity', 'sold_quantity', 'manufacturer']
    list_filter = ['category', 'manufacturer']
    fields = ['name', 'category', 'selling_price', 'purchase_price', 'description', 'image', 'quantity', 'manufacturer', 'sold_quantity']


class ProviderAdmin(admin.ModelAdmin):
    model = Provider
    list_display = ('name', 'email', 'phone_number', 'contact_person')

class GoodCategoryAdmin(admin.ModelAdmin):
    model = GoodCategory
    list_display = ('name',)


class SupplyAdmin(admin.ModelAdmin):
    model = Supply
    list_display = ('id', 'supply_date', 'provider')
    list_filter = ('supply_date', 'provider')
    search_fields = ('provider__name',)

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline]
    list_display = ('sale_date', 'discount', 'payment_method', 'final_cost')
    readonly_fields = ('final_cost',)

class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'good', 'quantity')

admin.site.register(Provider, ProviderAdmin)
admin.site.register(GoodCategory, GoodCategoryAdmin)
admin.site.register(Good, GoodAdmin)
admin.site.register(Supply, SupplyAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem, SaleItemAdmin)


