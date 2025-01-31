from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomePageView,
    AboutPageView,
    SignInPageView,
    ForgotPassPageView,
    ProductListView,
    ProductDetailView,
    UserRegistrationView,
    ProfileView,
    ChangePasswordView,
    DeleteAccountView,
    menu_view,
    add_to_cart,
    cart_view,
    update_cart,
    remove_from_cart,
    place_order,
    order_tracking,
    cancel_order,
    AdminDashboardView,
    AddProductView,
    manage_orders,
    update_order_status,
    EditProductView,
    delete_product,
)
from . import views  

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('forgotpass/', ForgotPassPageView.as_view(), name='forgotpass'),
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('menu/', menu_view, name='menu'),
    path('product-detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # ✅ Fix logout redirect
    path('profile/', ProfileView.as_view(), name='profile'),
    path('changepass/', ChangePasswordView.as_view(), name='changepass'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
    path('signin/', SignInPageView.as_view(), name='signin'),
    path('filter-products/', views.filter_products, name='filter_products'),
    path("add-to-cart/", add_to_cart, name="add_to_cart"),
    path('cart/', views.cart_view, name='cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('place_order/', place_order, name='place_order'),
    path('orders/', order_tracking, name='order_tracking'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('add-product/', AddProductView.as_view(), name='add_product'),
    path('ordersmanage/', manage_orders, name='manage_orders'),
    path('orders/update/<int:user_id>/', update_order_status, name='update_order_status'),
    path('product/edit/<int:pk>/', EditProductView.as_view(), name='edit_product'),
    path('remove-order/<int:order_id>/', views.remove_order, name='remove_order'),
    path('delete-product/<int:pk>/', delete_product, name='delete_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
