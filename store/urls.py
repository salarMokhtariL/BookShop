from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='processOrder'),
    path('team/', views.team_views, name='team'),
    path('author/', views.author_views, name='author'),
    path('sort/', views.sort_page, name='sort_page'),
    path('search/<slug:category_slug>/', views.category_list, name='category_list'),
    path('book/<slug:slug>/', views.product_detail, name='product_detail'),
    path('language/<slug:language_slug>/', views.language_list, name='language_list'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout, name='logout'),

]
