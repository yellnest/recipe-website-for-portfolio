from rest_framework import permissions

from recipe.models import *


class DataMixin:
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_recipe_queryset(self):
        recipe_slug = self.kwargs['recipe_slug'].lower()
        recipe = Recipe.objects.get(slug=recipe_slug)
        return recipe

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


