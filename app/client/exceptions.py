class PayPalAPIException(Exception):
    pass


class SubscriptionNotDeletedException(PayPalAPIException):
    def __init__(self):
        super().__init__('Subscription has not been deleted!')
