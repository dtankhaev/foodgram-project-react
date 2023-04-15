from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Кастомный пагинатор для выдачи рецептов.
    Добавлен параметр 'limit' (какое число объектов вернётся).
    Также установлена выдача по 5 записей.
    """

    page_size = 5
    page_size_query_param = 'limit'
