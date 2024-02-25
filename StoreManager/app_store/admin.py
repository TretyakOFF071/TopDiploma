from django.contrib import admin
from .models import Profile, GoodCategory, Provider, Good, SupplyItem, Supply


# Настройка отображения моделей в админке
class GoodAdmin(admin.ModelAdmin):
    model = Good
    list_display = ['name', 'category', 'selling_price', 'purchase_price', 'description', 'image', 'quantity', 'provider', 'activity_flag']
    list_filter = ['category', 'activity_flag', 'provider']
    actions = ['mark_as_active', 'mark_as_inactive']
    fields = ['name', 'category', 'selling_price', 'purchase_price', 'description', 'image', 'quantity', 'provider',
              'activity_flag']
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': (
            'name', 'category', 'selling_price', 'purchase_price', 'description', 'image', 'quantity', 'provider',
            'activity_flag'),
        }),
    ]


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'contact_person')

class GoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SupplyItemInline(admin.TabularInline):
    model = SupplyItem
    extra = 1

class SupplyAdmin(admin.ModelAdmin):
    inlines = [SupplyItemInline]

admin.site.register(Provider, ProviderAdmin)
admin.site.register(GoodCategory, GoodCategoryAdmin)
admin.site.register(Supply, SupplyAdmin)
admin.site.register(Good, GoodAdmin)