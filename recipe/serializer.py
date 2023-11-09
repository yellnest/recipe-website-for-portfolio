from rest_framework import serializers

from .models import *


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """ Serializer кол-ва ингредиентов
    """

    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'quantity')

    def to_representation(self, instance):
        rep = super(RecipeIngredientSerializer, self).to_representation(instance)
        rep['ingredient_name'] = instance.ingredient.name
        return rep


class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer рецептов
    """
    # ingredients = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='recipeingredient-detail')
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'slug', 'description', 'instructions', 'image', 'date_created', 'user', 'published',
                  'ingredients',)


class IngredientSerializer(serializers.ModelSerializer):
    """ Serializer ингредиентов
    """

    class Meta:
        model = Ingredient
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    """ Serializer рейтинга
    """
    # recipe_name = serializers.CharField(source='recipe.name')
    # username = serializers.CharField(source='user.username')
    recipe = serializers.SlugRelatedField(slug_field='slug', queryset=Recipe.objects.all())
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Rating
        fields = ('id', 'value', 'recipe', 'user', 'date_created')
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    """ Serializer избранного
    """

    class Meta:
        model = RecipeFavorite
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    """ Serializer регистрации
    """
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        password2 = validated_data['password2']
        if password2 != password:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """ Serializer пользователя
    """

    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """ Serializer комментариев
    """
    recipe = serializers.SlugRelatedField(slug_field='slug', queryset=Recipe.objects.all())
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'recipe', 'user', 'content', 'date_created',)
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }
