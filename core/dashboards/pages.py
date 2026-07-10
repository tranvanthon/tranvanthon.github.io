from enum import StrEnum


class CustomerPage(StrEnum):
    OVERVIEW = "overview"
    PRODUCTS = "products"
    ORDERS = "orders"
    WISHLIST = "wishlist"
    ADDRESS = "address"
    COUPONS = "coupons"
    SETTINGS = "settings"
    ACCOUNT = "account"
