from django.urls import path
from store import views

app_name = "store"

urlpatterns = [
    # Dashboard
    path(
        "dashboard/admin/", views.DashboardAdminView.as_view(), name="admin_dashboard"
    ),
    path(
        "dashboard/staff/", views.DashboardStaffView.as_view(), name="staff_dashboard"
    ),
    path(
        "dashboard/customer/",
        views.DashboardCustomerView.as_view(),
        name="customer_dashboard",
    ),
    path(
        "dashboard/customer/<str:page>/",
        views.DashboardCustomerPageView.as_view(),
        name="customer_partial",
    ),
    path(
        "dashboard/customer/overview/",
        views.DashboardCustomerOverviewView.as_view(),
        name="customer_overview",
    ),
    path(
        "dashboard/customer/orders/",
        views.DashboardCustomerOrdersView.as_view(),
        name="customer_orders",
    ),
    path(
        "dashboard/customer/products/",
        views.DashboardCustomerProductsView.as_view(),
        name="customer_products",
    ),
    path(
        "dashboard/customer/wishlist/",
        views.DashboardCustomerWishlistView.as_view(),
        name="customer_wishlist",
    ),
    path(
        "dashboard/customer/coupons/",
        views.DashboardCustomerCouponsView.as_view(),
        name="customer_coupons",
    ),
    path(
        "dashboard/customer/address/",
        views.DashboardCustomerAddressView.as_view(),
        name="customer_address",
    ),
    path(
        "dashboard/customer/settings/",
        views.DashboardCustomerSettingsView.as_view(),
        name="customer_settings",
    ),
    path(
        "dashboard/customer/account/",
        views.DashboardCustomerAccountView.as_view(),
        name="customer_account",
    ),
    # Quản lý Đa ảnh (Images)
    path("image/<int:pk>/main/", views.set_main_image, name="set_main_image"),
    # cart
    path("cart/detail/", views.cart_detail, name="cart_detail"),
    # basic
    path("search/", views.search, name="search"),
    path("", views.HomeView.as_view(), name="home"),
    # Quản lý Sản phẩm (Products)
    path("cart/add/<slug:slug>/", views.add_to_cart, name="add_to_cart"),
    path(
        "product/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"
    ),
    path(
        "product/<slug:slug>/update/",
        views.ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "product/<slug:slug>/delete/",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path("products/create/", views.ProductCreateView.as_view(), name="product_create"),
    # Quản lý Danh mục(Category)
    path("category/trash/", views.CategoryTrashView.as_view(), name="category_trash"),
    path(
        "category/create/", views.CategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "category/<slug:slug>/update/",
        views.CategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "category/<slug:slug>/detail/",
        views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    # soft delete
    path(
        "category/<slug:slug>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category_delete",
    ),
    # restore
    path(
        "category/<slug:slug>/restore/",
        views.CategoryRestoreView.as_view(),
        name="category_restore",
    ),
    # hard delete
    path(
        "category/<slug:slug>/hard-delete/",
        views.CategoryPermanentDeleteView.as_view(),
        name="category_permanent_delete",
    ),
    path("brand/create/", views.BrandCreateView.as_view(), name="brand_create"),
]
