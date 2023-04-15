# from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Recipe
from rest_framework import viewsets

from .paginations import CustomPagination
from .permissions import AuthorOrReadOnly
from .serializers import ReadRecipeSerializer, WriteRecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    # filter_backends = (DjangoFilterBackend,)  # РАЗОБРАТЬСЯ
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadRecipeSerializer
        return WriteRecipeSerializer
