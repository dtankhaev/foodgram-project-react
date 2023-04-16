# from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.serializers import LittleRecipeSerializer

from .paginations import CustomPagination
from .permissions import AuthorOrReadOnly
from .serializers import (IngredientSerializer, ReadRecipeSerializer,
                          ReadTagSerializer, WriteRecipeSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет рецептов, применяющий 2 сериализатора:
    ReadRecipeSerializer/WriteRecipeSerializer (чтение/запись)
    с применением кастомного пермишена AuthorOrReadOnly,
    кастомного пагинатора CustomPagination.

    Добавлено три дополнительных роута (@action):
     - /api/recipes/{id}/favorite/ ('POST', 'DELETE')
        (добавление/удаление рецепта из избранного)
     - /api/recipes/{id}/shopping_cart/ ('POST', 'DELETE')
        (добавление/удаление рецепта из списка покупок)
     - /api/recipes/download_shopping_cart/ ('GET')
        (скачивание списка покупок).
    """
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    # filter_backends = (DjangoFilterBackend,)  # TODO создать фильтры
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadRecipeSerializer
        return WriteRecipeSerializer

    @action(detail=True,
            methods=('POST', 'DELETE',),
            permission_classes=(IsAuthenticated,)
            )
    def favorite(self, request, pk=None):
        """Добавление рецепта в избранное."""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self.add_my_obj(Favorite, recipe, request.user)
        return self.delete_my_obj(Favorite, recipe, request.user)

    @action(detail=True,
            methods=('POST', 'DELETE'),
            permission_classes=(IsAuthenticated,)
            )
    def shopping_cart(self, request, pk=None):
        """Добавление рецепта в список покупок."""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self.add_my_obj(ShoppingCart, recipe, request.user)
        return self.delete_my_obj(ShoppingCart, recipe, request.user)

    def add_my_obj(self, model, recipe, user):
        """
        Метод, предназначенный для добавления рецепта,
        в Избранное/Список покупок.
        применяется только в методах favorite и shopping_cart.
        """

        if model.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                    {'errors': f'рецепт уже добавлен в {model.__name__}'},
                    status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=user, recipe=recipe)
        serializer = LittleRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_my_obj(self, model, recipe, user):
        """
        Метод, предназначенный для удаления рецепта,
        из избранного/списка покупок.
        применяется только в методах favorite и shopping_cart.
        """

        obj = model.objects.filter(user=user, recipe=recipe)
        if obj.exists():
            obj.delete()
            return Response(
                    {'successfully': f'успешно удален из {model.__name__}'},
                    status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': f'рецепта нет в списке {model.__name__}'},
                        status=status.HTTP_400_BAD_REQUEST)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для отображения ингредиентов (модель Ingredient).
    Доступен всем только для чтения.
    Подключен встроенный фильтрующий поисковой бэкенд по полю 'name'.
    api/ingredients/?search=л (выдаст все ингредиенты начинающиеся на 'л').
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для отображения тегов (модель Tag).
    Доступен всем только для чтения.
    api/tags/.
    """

    queryset = Tag.objects.all()
    serializer_class = ReadTagSerializer
