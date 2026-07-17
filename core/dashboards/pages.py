from enum import StrEnum


class CustomerPage(StrEnum):
    SIDEBAR = "sidebar"
    OVERVIEW = "overview"
    PRODUCTS = "products"
    ORDERS = "orders"
    WISHLIST = "wishlist"
    ADDRESS = "address"
    COUPONS = "coupons"
    SETTINGS = "settings"
    ACCOUNT = "account"
