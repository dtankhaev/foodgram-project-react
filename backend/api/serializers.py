from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from users.serializers import CustomUserSerializer


class WriteIngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientAmount
        fields = ('id',
                  'amount')


class WriteRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания рецептов!(модель Recipe),
    с вложенным сериализатором WriteIngredientAmountSerializer

    Применен Base64ImageField для картинок.
    """

    ingredients = WriteIngredientAmountSerializer(many=True)
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(),
                                        slug_field='id',
                                        many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        exclude = ('author',)

    def create_ingredients(self, recipe, ingredients):
        """Данный метод предназачен для создания объекта IngredientAmount.
        применяется только в методах create, update
        """

        IngredientAmount.objects.bulk_create(
            [IngredientAmount(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients(instance, ingredients)
        instance.save
        return instance

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise ValidationError({'Нужен хотя бы один ингредиент!'})
        ingredients_list = []
        for obj in ingredients:
            ingredient = get_object_or_404(Ingredient, id=obj['id'])
            if ingredient in ingredients_list:
                raise ValidationError({'Ингредиенты не должны повторяться!'})
            if int(obj['amount']) <= 0:
                raise ValidationError(
                    {'Количество ингредиента должно быть больше 0!'}
                                     )
            ingredients_list.append(ingredient)
        return ingredients

    def to_representation(self, instance):
        return ReadRecipeSerializer(
                    instance,
                    context={'request': self.context.get('request')}
                                    ).data


class ReadIngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения модели IngredientAmount.
    Извлекаются дополнительные поля id, name, measurement_unit ингредиента.

    Данный сериализатор применяется только в ReadRecipeSerializer.
    """

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
                                    source='ingredient.measurement_unit'
                                    )

    class Meta:
        model = IngredientAmount
        fields = ('id',
                  'name',
                  'measurement_unit',
                  'amount')


class ReadTagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для тегов (модель Tag)
    Только для чтения.
    """

    class Meta:
        model = Tag
        fields = ('id',
                  'name',
                  'color',
                  'slug')


class ReadRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения рецептов! модель Recipe.
    с 2 вложенными сериализаторами:
     - CustomUserSerializer (выдача пользователя)
     - ReadIngredientAmountSerializer (выдача ингредиента с кол-ом)

    Применен Base64ImageField для картинок.

    Также создано 2 новых поля:
     - is_favorited (в избранном ли рецепт?)
     - is_in_shopping_cart (в корзине ли рецепт?).
    """

    author = CustomUserSerializer()
    ingredients = ReadIngredientAmountSerializer(many=True,
                                                 source='recipe_ingredient',)
    tags = ReadTagSerializer(many=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'name',
                  'author',
                  'image',
                  'text',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'tags',
                  'cooking_time',
                  'pub_date')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов (модель Ingredient)
    Только для чтения.
    """

    class Meta:
        model = Ingredient
        fields = ('id',
                  'name',
                  'measurement_unit',)
