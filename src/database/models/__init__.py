
from .base_model import Base
from .telegram_user import TelegramUser
from .partner_channel import PartnerChannel
from .hamster_code import HamsterCode
from .statistic import Statistic
from .confidential_data import ConfidentialData
from .product import Product
from .subscription import Subscription
from .payment import Payment
from .hamster_claimer import HamsterClaimer

__all__ = (
    'Base',
    'TelegramUser',
    'PartnerChannel',
    'HamsterCode',
    'Statistic',
    'ConfidentialData',
    'Product',
    'Subscription',
    'Payment',
    'HamsterClaimer'
)

# Relationships:
# TelegramUser to Subscription: One-to-Many (A user can have many subscriptions).
# TelegramUser to Payment: One-to-Many (A user can have many payments).
# Subscription to Product: Many-to-One (A subscription relates to one product).
# Payment to Subscription: Many-to-One (A payment can relate to one subscription).
