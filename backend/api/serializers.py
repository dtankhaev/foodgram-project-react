from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, IngredientAmount, Recipe, Tag
from rest_framework import serializers
from users.serializers import CustomUserSerializer


class WriteIngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientAmount
        fields = ('id',
                  'amount')


class WriteRecipeSerializer(serializers.ModelSerializer):
    ingredients = WriteIngredientAmountSerializer(many=True)
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(),
                                        slug_field='id',
                                        many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        exclude = ('author',)

    def for_create_ingredients(self, recipe, ingredients):
        for ingredient in ingredients:
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.for_create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.for_create_ingredients(instance, ingredients)
        instance.save
        return instance

    def to_representation(self, instance):
        return ReadRecipeSerializer(
                    instance,
                    context={'request': self.context.get('request')}
                    ).data


class ReadIngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
                                    source='ingredient.measurement_unit'
                                    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id',
                  'name',
                  'measurement_unit',
                  'amount')


class ReadTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id',
                  'name',
                  'color',
                  'slug')


class ReadRecipeSerializer(serializers.ModelSerializer):
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
