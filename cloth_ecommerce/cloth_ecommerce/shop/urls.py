from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.shop, name='shop'), 
    path('clothy4kids/', views.clothy4kids, name='clothy4kids'),
    path('clothy4men/', views.clothy4men, name='clothy4men'),
    path('clothy4women/', views.clothy4women, name='clothy4women'),
    path('kids/', views.clothy4kids, name='clothy4kids'),
    path('men/', views.clothy4men, name='clothy4men'),
    path('women/', views.clothy4women, name='clothy4women'),
    path('search/', views.search_products, name='search'),
    path('reviews/', views.reviews, name='reviews'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    #path('add-to-cart-ajax/', views.add_to_cart_ajax, name='add_to_cart_ajax'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:product_id>/',views.update_cart, name='update_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('forget_password/', views.forget_password, name='forget_password'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)