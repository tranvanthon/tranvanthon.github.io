from core.dashboards.configs import DashboardPageConfig
from core.dashboards.context import (
    account_context,
    address_context,
    coupons_context,
    overview_context,
    product_context,
    settings_context,
    wishlist_context,
)
from core.dashboards.pages import CustomerPage

OVERVIEW = DashboardPageConfig(
    page=CustomerPage.OVERVIEW,
    title="Tổng quan",
    icon="bi bi-speedometer2",
    template="partials/dashboard/overview.html",
    context=overview_context,
)
ACCOUNT = DashboardPageConfig(
    page=CustomerPage.ACCOUNT,
    title="Tài khoản",
    icon="bi bi-person-circle",
    template="partials/dashboard/account_info.html",
    context=account_context,
)
PRODUCTS = DashboardPageConfig(
    page=CustomerPage.PRODUCTS,
    title="Sản phẩm",
    icon="bi bi-box-seam",
    template="partials/dashboard/products.html",
    context=product_context,
)
ORDERS = DashboardPageConfig(
    page=CustomerPage.ORDERS,
    title="Đơn hàng",
    icon="bi bi-receipt",
    template="partials/dashboard/order_history.html",
    context=product_context,
)
WISHLIST = DashboardPageConfig(
    page=CustomerPage.WISHLIST,
    title="Sản phẩm yêu thích",
    icon="bi bi-heart",
    template="partials/dashboard/wishlist.html",
    context=wishlist_context,
)
ADDRESS = DashboardPageConfig(
    page=CustomerPage.ADDRESS,
    title="Sổ địa chỉ",
    icon="bi bi-geo-alt",
    template="partials/dashboard/address_book.html",
    context=address_context,
)
SETTINGS = DashboardPageConfig(
    page=CustomerPage.SETTINGS,
    title="Cài đặt",
    icon="bi bi-gear",
    template="partials/dashboard/settings.html",
    context=settings_context,
)
COUPONS = DashboardPageConfig(
    page=CustomerPage.COUPONS,
    title="Mã giảm giá (Marketing)",
    icon="bi bi-ticket-perforated",
    template="partials/dashboard/coupons.html",
    context=coupons_context,
)

CUSTOMER_PAGES = {
    CustomerPage.OVERVIEW: OVERVIEW,
    CustomerPage.ORDERS: ORDERS,
    CustomerPage.ACCOUNT: ACCOUNT,
    CustomerPage.COUPONS: COUPONS,
    CustomerPage.PRODUCTS: PRODUCTS,
    CustomerPage.WISHLIST: WISHLIST,
    CustomerPage.SETTINGS: SETTINGS,
    CustomerPage.ADDRESS: ADDRESS,
}
