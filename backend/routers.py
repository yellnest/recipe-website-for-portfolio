from rest_framework.routers import DefaultRouter

from recipe.views import *

router = DefaultRouter()

router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recidit', RecipeIngredientViewSet)
router.register(r'favorite', RecipeFavoriteViewSet)


urlpatterns = router.urls
