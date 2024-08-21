from pydantic import BaseModel


class PartnerChannelSchema(BaseModel):
    channel_link: str
    channel_id: int
    name: str


class PaymentPayload(BaseModel):
    user_id: int
    invoice_id: str
    product_name: str
    amount: float
    payment_service: str
