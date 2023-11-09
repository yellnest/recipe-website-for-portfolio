from rest_framework import permissions, generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import *
from .permission import IsAdminUserOrReadOnly
from .serializer import RecipeSerializer, IngredientSerializer, RecipeIngredientSerializer, RatingSerializer, \
    RecipeFavoriteSerializer, RegisterSerializer, UserSerializer, CommentSerializer
from .utils import GetQuerySetMixin, PermissionMixin


class RecipeViewSet(ModelViewSet):
    """Вывод списка рецептов
    """
    queryset = Recipe.objects.filter(published=True)
    serializer_class = RecipeSerializer
    lookup_field = 'slug'

    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    filter_fields = ('name', 'date_created')

    permission_classes = (IsAdminUserOrReadOnly,)


class IngredientViewSet(PermissionMixin, ModelViewSet):
    """Вывод списка ингредиентов
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'slug'

    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class RecipeIngredientViewSet(PermissionMixin, ModelViewSet):
    """Добавление описания о количестве ингредиента к рецепту
    """
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer


class RatingView(GetQuerySetMixin, generics.ListCreateAPIView):
    """Вывод списка ретинга
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    filter_fields = ('value',)

    def get_queryset(self):
        return Rating.objects.filter(recipe=self.get_recipe_slug())


class RecipeFavoriteViewSet(ModelViewSet):
    """Вывод списка избранного блюда пользователя
    """
    queryset = RecipeFavorite.objects.all()
    serializer_class = RecipeFavoriteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return self.request.user.favorite_recipes.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterView(generics.GenericAPIView):
    """Регистрация пользователя
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'Пользователь успешно зарегистрирован'
        })


class CommentView(GetQuerySetMixin, generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(recipe=self.get_recipe_slug())

