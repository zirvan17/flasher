"""
Constant api URLs
"""

PREFIX = "https://shopee.co.id"
MALL_PREFIX = "https://mall.shopee.co.id"
PATHS = {
    "auth_login": "/api/v2/authentication/login",
    "auth_otp": "/api/v2/authentication/resend_otp",
    "auth_vcode": "/api/v2/authentication/vcode_login",
    "account_info": "/api/v1/account_info",
    "get_item": "/api/v2/item/get?itemid=%i&shopid=%i",
    "add_to_cart": "/api/v4/cart/add_to_cart",
    "checkout_get": "/api/v2/checkout/get",
    "checkout": "/api/v2/checkout/place_order"
}
