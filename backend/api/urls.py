from django.urls import include, path

registration = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('auth/', include(registration)),
]
