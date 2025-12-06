from django.contrib import admin
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductImageInline


# Register your models here.
class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']
    extra = 0
    
    
class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline , ProductImageInline]


admin.site.unregister(Product)
admin.site.register(Product , CustomProductAdmin)

