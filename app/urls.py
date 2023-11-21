from django.urls import path

from api.views import UpdateCatalog, ModelsList
from catalog.views import add_catalog, index

urlpatterns = [
    path('', index),
    path('catalog', add_catalog),
    path('models', ModelsList.as_view(), name='models-list'),
    path('update_autoru_catalog', UpdateCatalog.as_view(), name='update_autoru_catalog'),
]
