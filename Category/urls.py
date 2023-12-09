from django.urls import path
from Category.views import CategoryApiHandler, CategoryListApiHandler

urlpatterns = [
    path('', CategoryApiHandler.as_view(), name='category_handler'),
    path('<int:category_id>', CategoryApiHandler.as_view(), name='category_detail_handler'),
    path('list', CategoryListApiHandler.as_view(), name='category_list_handler'),
]
