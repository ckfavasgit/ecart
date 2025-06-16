from enum import Enum

class MessageEnum(Enum):
    LOGIN_SUCCESS = 'Login successful'
    LOGIN_FAILED = 'Login failed'
    LOGOUT_SUCCESS = 'Token revoked successfully.'
    LOGOUT_FAILED = 'Logout failed'
    USERNAME_REQUIRED = 'Username is required.'
    PASSWORD_REQUIRED = 'Password is required.'
    TOKEN_REQUIRED = 'No token provided.'
    PRODUCT_LIST_SUCCESS = 'Product list fetched successfully.'
    PRODUCT_DETAIL_SUCCESS = 'Product details fetched successfully.'
    PRODUCT_NOT_FOUND = 'Product not found.'
