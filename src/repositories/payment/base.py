from abc import ABC, abstractmethod

from src.database.models import Payment


class IPaymentRepository(ABC):
    model = None

    @abstractmethod
    async def create_payment(
            self, user_id: int,
            subscription_id: int,
            amount: float,
            payment_service: str,
            invoice_id: str
    ) -> Payment:
        ...


