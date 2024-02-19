from django.contrib import admin
from .models import Profile, GoodCategory, Provider, Good




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
admin.site.register(Good, GoodAdmin)