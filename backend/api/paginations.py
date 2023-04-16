from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Кастомный пагинатор для выдачи рецептов.
    Добавлен параметр 'limit' (какое число объектов вернётся).
    Также установлена выдача по 6 записей.
    """

    page_size = 6
    page_size_query_param = 'limit'
