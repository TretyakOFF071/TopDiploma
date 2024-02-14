from django.contrib import admin
from .models import Customer, GoodCategory, Good, Provider


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ['user']

class ProviderAdmin(admin.ModelAdmin):
    model = Provider
    list_display = ['name']

class CategoryAdmin(admin.ModelAdmin):

    model = GoodCategory
    list_display = ['name']


class GoodsInLine(admin.TabularInline):
    model = Good
    extra = 1

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

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.groups.filter(name='Менеджеры').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='Менеджеры').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.groups.filter(name='Менеджеры').exists()

    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.groups.filter(name='Менеджеры').exists()
    def mark_as_active(self, queryset):
        queryset.update(activity_flag='a')
    def mark_as_inactive(self, queryset):
        queryset.update(activity_flag='i')

    mark_as_active.short_description = 'Пометить как активные'
    mark_as_inactive.short_description = 'Переместить в стоп-лист'



admin.site.register(Customer, CustomerAdmin)
admin.site.register(GoodCategory, CategoryAdmin)
admin.site.register(Good, GoodAdmin)
admin.site.register(Provider, ProviderAdmin)
