from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorOrReadOnly(BasePermission):
    """
    Кастомный пермишн предназначенный только для RecipeViewSet (рецептов).
    Только автор может удалять/изменять рецепты.
    Читать - любой пользователь.
    Создавать - зарегистрированный.
    """

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)
