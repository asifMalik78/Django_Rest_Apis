from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count
from django.contrib.contenttypes.admin import GenericTabularInline
from django.urls import reverse
from django.utils.html import format_html
from urllib.parse import urlencode
from tags.models import TaggedItem
from core.models import User
from . import models
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ['username__istartswith']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "usable_password", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )
  
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self , request , model_admin):
        return [
            ('<10', 'Low'),
            ('>10', 'High'),
            ('>100', 'Very High'),
        ]
        
    def queryset(self , request , queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        elif self.value() == '>10':
            return queryset.filter(inventory__gt=10)
        elif self.value() == '>100':
            return queryset.filter(inventory__gt=100)
        return queryset

class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 0
    readonly_fields = ['thumbnail']

    def thumbnail(self , instance):
        if instance.image.name != '':
            return format_html(f'<img src="{instance.image.url}" alt="{instance.image.name}" class="thumbnail" />')
        return ''
 
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }

    actions = ['clear_inventory']
    inlines = [ProductImageInline]
    list_display = ['title' , 'description' , 'slug' , 'inventory_status' , 'unit_price' , 'collection_title' , 'updated_at' , 'created_at']
    list_editable = ['description' , 'slug' , 'unit_price']
    list_select_related = ['collection']
    list_per_page = 5
    list_filter = [InventoryFilter , 'collection' , 'updated_at']
    search_fields = ['title__istartswith']
    
    @admin.display(ordering = 'inventory')
    def inventory_status(self , product):
        if product.inventory < 10:
            return 'Low'
        return 'High'
    
    def collection_title(self , product):
        return product.collection.title if product.collection else 'No Collection'
    
    @admin.action(description = 'Clear Inventory')
    def clear_inventory(self , request , queryset):
        queryset.update(inventory=0)
        self.message_user(request , 'Inventory cleared')

    class Media:
        css = {
            'all': ('store/styles.css',)
        }

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title' , 'products_count']
    list_per_page = 5
    search_fields = ['title__istartswith']
    autocomplete_fields = ['featured_product']
    
    @admin.display(ordering = 'products_count')
    def products_count(self , collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': collection.id})
        return format_html('<a href="{}">{}</a>' , url, collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('products'))

    
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id' , 'first_name' , 'last_name' , 'membership' , 'orders_count']
    list_editable = ['membership']
    list_per_page = 5
    ordering = ['user__first_name' , 'user__last_name']
    search_fields = ['user__first_name__istartswith' , 'user__last_name__istartswith']
    autocomplete_fields = ['user']
    list_filter = ['membership']
    list_select_related = ['user']
    
    @admin.display(ordering = 'orders_count')
    def orders_count(self , customer):
        url = reverse('admin:store_order_changelist') + '?' + urlencode({'customer__id': customer.id})
        return format_html('<a href="{}">{}</a>' , url, customer.orders_count)
    
    def get_queryset(self , request):
        return super().get_queryset(request).annotate(orders_count=Count('order'))
    
    
class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 2
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['id' , 'placed_at' , 'payment_status' , 'customer_name']
    list_select_related = ['customer']
    list_per_page = 5
    inlines = [OrderItemInline]
    
    def customer_name(self , order):
        return order.customer.user.first_name + ' ' + order.customer.user.last_name if order.customer.user else '-' 

# admin.site.register(models.Collection)
