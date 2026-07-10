from core.dashboards.pages import CustomerPage


def overview_context(request):
    return {}


def wishlist_context(request):
    return {}


def account_context(request):
    return {}


def orders_context(request):
    return {}


def address_context(request):
    return {}


def product_context(request):
    return {}


def product_settings_context(request):
    return {}


def settings_context(request):
    return {}


def admin_settings_context(request):
    return {}


def category_settings_context(request):
    return {}


def report_context(request):
    return {}


def coupons_context(request):
    return {}


def order_history_context(request):
    return {}


CUSTOMER_CONTEXTS = {
    CustomerPage.OVERVIEW: overview_context,
    CustomerPage.ORDERS: orders_context,
    CustomerPage.PRODUCTS: product_context,
    CustomerPage.WISHLIST: wishlist_context,
    CustomerPage.COUPONS: coupons_context,
    CustomerPage.ADDRESS: address_context,
    CustomerPage.ACCOUNT: account_context,
    CustomerPage.SETTINGS: settings_context,
}
