from django.contrib import admin
from .models import Category, Product, ProductImage

from django.utils.safestring import mark_safe
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepoluated_fields = {'slug': ('name',)}


class ImageInline(admin.TabularInline):
    model = ProductImage
    list_display = ['order',]
    list_editable = ['order',]
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.image:
            return mark_safe('<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format(obj.image.url))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'category', 'created', 'updated']
    list_editable = ['price', 'available']
    prepoluated_fields = {'slug': ('name',)}
    inlines = [ImageInline]


# https://www.djangosnippets.org/snippets/1053/
# An easy way of making inlines orderable using drag-and-drop, using jQuery UI's sortable() plugin.
#
# First, add an "order" field to the inline models which is an IntegerField, and set that model to use 'order' as its default order_by.
#
# Then hook in the JavaScript. This should make them drag-and-drop sortable using jQuery UI, and also hide the divs containing those order
# fields once the page has loaded. This technique is unobtrusive: if JavaScript is disabled, the order fields will be visible and the user
# will be able to manually set the order by entering numbers themselves.

# admin.py

# from django.contrib import admin
# from django import forms
#
# from models import Menu, Item
#
# class MenuForm(forms.ModelForm):
#     model = Menu
#     class Media:
#         js = (
#             '/static/js/jquery-latest.js',
#             '/static/js/ui.base.js',
#             '/static/js/ui.sortable.js',
#             '/static/js/menu-sort.js',
#         )
#
# class ItemInline(admin.StackedInline):
#     model = Item
#
# admin.site.register(Menu,
#     inlines = [ItemInline],
#     form = MenuForm,
# )

# """
# /* menu-sort.js */
#
# jQuery(function($) {
#     $('div.inline-group').sortable({
#         /*containment: 'parent',
#         zindex: 10, */
#         items: 'div.inline-related',
#         handle: 'h3:first',
#         update: function() {
#             $(this).find('div.inline-related').each(function(i) {
#                 if ($(this).find('input[id$=name]').val()) {
#                     $(this).find('input[id$=order]').val(i+1);
#                 }
#             });
#         }
#     });
#     $('div.inline-related h3').css('cursor', 'move');
#     $('div.inline-related').find('input[id$=order]').parent('div').hide();
# });
# """
