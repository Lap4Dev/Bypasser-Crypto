from pydantic import BaseModel


class PartnerChannelSchema(BaseModel):
    channel_link: str
    channel_id: int
    name: str
