from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/register', views.UserRegistrationView.as_view(), name='register'),
    path('user/login', views.UserLoginView.as_view(), name='login'),

    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/add_for_sell', views.ProductSellView.as_view(), name='add_selling_product'),
    path('products/purchase/<int:id>', views.PurchaseCreateView.as_view(), name='purchase_product')
]
