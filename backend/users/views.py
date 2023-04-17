from api.paginations import CustomPagination
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Subscribe
from .serializers import SubscribeSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """
    Кастомный вьюсет пользователей (User)
    Добавлен дополнительный роут для отображения подписок пользователя
    и роут для подписки/отписки на пользователей,
    с применением кастомной пагинации CustomPagination.
    """

    pagination_class = CustomPagination

    @action(detail=False)
    def subscriptions(self, request):
        """
        Отображение подписок текущего пользователя
        api/users/subscriptions/.
        """

        queryset = request.user.subscribers.all()
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(pages,
                                         many=True,
                                         context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=('POST', 'DELETE'))
    def subscribe(self, request, id=None):
        """
        Подписка/Отписка на пользователей.
        api/users/{id}/subscribe/.
        """

        author = get_object_or_404(User, id=id)
        if self.request.method == 'POST':  # TODO подумать как упростить.
            if self.request.user == author:
                return Response(
                    {'errors': 'Вы не можете подписаться на себя'},
                    status=status.HTTP_400_BAD_REQUEST)
            if Subscribe.objects.filter(user=self.request.user,
                                        author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на данного пользователя'},
                    status=status.HTTP_400_BAD_REQUEST)
            queryset = Subscribe.objects.create(user=self.request.user,
                                                author=author)
            serializer = SubscribeSerializer(queryset,
                                             context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #  Начало DELETE запроса.
        if self.request.user == author:
            return Response({'errors': 'Вы пытаетесь отписаться от себя'},
                            status=status.HTTP_400_BAD_REQUEST)
        subscribe = Subscribe.objects.filter(user=self.request.user,
                                             author=author)
        if subscribe.exists():
            subscribe.delete()
            return Response({'successfully': 'Отписка совершена'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Вы уже отписаны от данного пользователя'},
                        status=status.HTTP_400_BAD_REQUEST)
