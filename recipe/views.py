from rest_framework import permissions, generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import *
from .permission import IsAdminUserOrReadOnly
from .serializer import RecipeSerializer, IngredientSerializer, RecipeIngredientSerializer, RatingSerializer, \
    RecipeFavoriteSerializer, RegisterSerializer, UserSerializer, CommentSerializer


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


class IngredientViewSet(ModelViewSet):
    """Вывод списка ингредиентов
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'slug'

    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    permission_classes = (permissions.IsAdminUser,)


class RecipeIngredientViewSet(ModelViewSet):
    """Добавление описания о количестве ингредиента к рецепту
    """
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer

    permission_classes = (permissions.IsAdminUser,)


class RatingView(generics.ListCreateAPIView):
    """Вывод списка ретинга
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filter_fields = ('value',)

    def get_queryset(self):
        recipe_slug = self.kwargs['recipe_slug'].lower()
        recipe = Recipe.objects.get(slug=recipe_slug)
        return Rating.objects.filter(recipe=recipe)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeFavoriteViewSet(ModelViewSet):
    """Вывод списка избранного блюда пользователя
    """
    queryset = RecipeFavorite.objects.all()
    serializer_class = RecipeFavoriteSerializer


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


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        recipe_slug = self.kwargs['recipe_slug'].lower()
        recipe = Recipe.objects.get(slug=recipe_slug)
        return Comment.objects.filter(recipe=recipe)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
