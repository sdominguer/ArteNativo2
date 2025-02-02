from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),

    # Rutas de productos
    path('products/', views.product_list, name='product_list'),
    path('products/new/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('productos/json/', views.product_list_json, name='product_list_json'),

    # Rutas de subastas
    path('auctions/', views.auction_list, name='auction_list'),
    path('auctions/new/<int:product_id>/', views.auction_create, name='auction_create'),

    # Rutas de carrito
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Rutas de autenticación
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('search/', views.search_product, name='search'),  # Añade esta línea
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
