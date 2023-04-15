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
    pagination_class = CustomPagination

    @action(detail=False)
    def subscriptions(self, request):
        queryset = Subscribe.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(pages,
                                         many=True,
                                         context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=('POST', 'DELETE'))
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        if self.request.method == 'POST':
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
            return Response({'succession': 'Отписка совершена'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Вы уже отписаны от данного пользователя'},
                        status=status.HTTP_400_BAD_REQUEST)
