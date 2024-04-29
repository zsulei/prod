from django.urls import path

from . import views
from .views import (ProductDetailView, ProductsListView, ProductUpdateView,
                    about, delete_all, get_sizes, parse_tsgoods_view,
                    search_by_name)

app_name = 'products'

urlpatterns = [

    # path('', index, name='index'),
    # path('category/<int:category_id>/', products2, name='test2'),
    # path('test/<int:page_number>/', products2, name='test'),
    # path('detail/<int:product_id>/', product, name='detail'),

    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:pk>/', ProductsListView.as_view(), name='category'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path('get-sizes/', get_sizes, name='get_sizes'),
    path('update_image/<int:pk>/', ProductUpdateView.as_view(), name='update_product_image'),

    path('about/', about, name='about'),
    path('search/', search_by_name, name='search'),

    path('parse-tsgoods/', parse_tsgoods_view, name='parse_tsgoods'),
    path('delete_all/', delete_all, name='delete'),
    # path('hide/', hide, name='hide'),
    path('strange/', views.strange_products, name='strange')

]
