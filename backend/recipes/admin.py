from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'pub_date', 'count_favorites',
                    'get_html_photo']
    list_editable = ['author', ]
    search_fields = ['name', ]
    list_filter = ['author', 'name', 'tags', 'pub_date']
    list_per_page = 6

    def count_favorites(self, obj):
        return obj.favorites.count()

    count_favorites.short_description = 'в избранном'

    def get_html_photo(self, object):
        return mark_safe(f"<img src='{object.image.url}' width=50>")


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit']
    search_fields = ['name', ]
    list_filter = ['name', ]


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'amount']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipe']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'slug']
