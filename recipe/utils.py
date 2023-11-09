from rest_framework import permissions
from rest_framework import serializers

from recipe.models import *


class GetQuerySetMixin:
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_recipe_slug(self):
        recipe_slug = self.kwargs['recipe_slug'].lower()
        recipe = Recipe.objects.get(slug=recipe_slug)
        return recipe

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PermissionMixin:
    permission_classes = (permissions.IsAdminUser,)




