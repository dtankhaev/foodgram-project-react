from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import ForRecipeFilter
from .paginations import CustomPagination
from .permissions import AuthorOrReadOnly
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from .serializers import (IngredientSerializer, ReadRecipeSerializer,
                          ReadTagSerializer, WriteRecipeSerializer)
from users.serializers import LittleRecipeSerializer


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


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет рецептов, применяющий 2 сериализатора:
    ReadRecipeSerializer/WriteRecipeSerializer (чтение/запись),
     - /api/recipes/ ('GET', 'POST', 'PATCH', 'DELETE')
    с применением кастомного пермишена AuthorOrReadOnly,
    и кастомного пагинатора CustomPagination.

    Подключен внешний бэкенд DjangoFilterBackend,
    с применением кастомного фильтра ForRecipeFilter
    по полям 'tags', 'author', 'is_favorited', 'is_in_shopping_cart'.
     - /api/recipes/?is_favorited=1 (отображение избранных рецептов)
     - /api/recipes/?is_in_shopping_cart=1 (отображение корзины покупателя)
     - /api/recipes/?author=1 (отображение рецептов определенного пользователя)
     - /api/recipes/?tags=breakfast (отображение рецептов с выбранным тегом)

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
    filter_backends = (DjangoFilterBackend,)
    pagination_class = CustomPagination
    filterset_class = ForRecipeFilter

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
            return self.add_obj(Favorite, recipe, request.user)
        return self.delete_obj(Favorite, recipe, request.user)

    @action(detail=True,
            methods=('POST', 'DELETE'),
            permission_classes=(IsAuthenticated,)
            )
    def shopping_cart(self, request, pk=None):
        """Добавление рецепта в корзину."""

        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self.add_obj(ShoppingCart, recipe, request.user)
        return self.delete_obj(ShoppingCart, recipe, request.user)

    def add_obj(self, model, recipe, user):
        """
        Метод, предназначенный для добавления рецепта,
        в избранное/список покупок.
        применяется только в методах favorite и shopping_cart.
        """

        if model.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                    {'errors': f'рецепт уже добавлен в {model.__name__}'},
                    status=status.HTTP_400_BAD_REQUEST)
        model.objects.create(user=user, recipe=recipe)
        serializer = LittleRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, recipe, user):
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

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        if not request.user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = IngredientAmount.objects.filter(
            recipe__shopping_cart__user=request.user).values(
                                                'ingredient__name',
                                                'ingredient__measurement_unit'
                                        ).annotate(all_amount=Sum('amount'))
        shopping_list = (f'Корзина: {request.user}\n\n'
                         f'Дата: {datetime.today():%Y-%m-%d}\n\n'
                         )
        shopping_list += '\n'.join([
                            f'- {ingredient["ingredient__name"]} '
                            f'({ingredient["ingredient__measurement_unit"]})'
                            f' - {ingredient["all_amount"]}'
                            for ingredient in ingredients
                            ])
        shopping_list += f'\n\nFoodgram ({datetime.today():%Y-%m-%d})'

        filename = 'shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
