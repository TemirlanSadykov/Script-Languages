from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-out/', views.sign_out, name='sign-out'),
    path('restricted/', views.restricted, name='restricted'),
    path('add-product/', views.add_product, name='add-product'),
    path('view-product/', views.view_product, name='view-product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit-product'),
    path('purchase-product/<int:product_id>/', views.purchase_product, name='purchase-product'),
    path('process-purchase/', views.process_purchase, name='process-purchase'),
    path('product-list/', views.product_list, name='product-list'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('become-seller/', views.become_seller, name='become-seller'),
]
