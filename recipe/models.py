from django.contrib.auth.models import User
from django.db import models

from recipe.base.servieces import path_to_recipe_upload_image


class Recipe(models.Model):
    """Модель рецепта
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True)
    description = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to=path_to_recipe_upload_image)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Ingredient(models.Model):
    """Модель Ингредиента
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class RecipeIngredient(models.Model):
    """Модель отношения Ингредиента к Рецепту и описания количества этого Ингредиента
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=50)

    def __str__(self):
        return self.quantity

    class Meta:
        verbose_name = 'Количество Ингредиентов'
        verbose_name_plural = 'Количество Ингредиентов'


class Comment(models.Model):
    """Модель комментария
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.content


class Rating(models.Model):
    """Модель рейтинга
    """
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField(choices=RATING_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class RecipeFavorite(models.Model):
    """Модель избранного блюда пользователя
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="favorites")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_recipes")

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = ('recipe', 'user')
