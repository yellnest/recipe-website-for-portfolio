from django.contrib import admin
from .models import *


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'description', 'instructions', 'date_created', 'user', 'published', )
    list_display_links = ('id', 'name')
    list_editable = ('published',)
    list_filter = ('date_created', 'name', 'id')
    search_fields = ('name', 'user')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'quantity')
    list_display_links = ('id', 'quantity')


@admin.register(RecipeFavorite)
class RecipeFavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')
    list_display_links = ('id', 'user', 'recipe')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user', 'value')
    list_display_links = ('id', 'user', 'recipe', 'value')
    list_filter = ('value',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user', 'content', 'date_created')
    list_display_links = ('id', 'user', 'recipe')
