from pydantic import BaseModel


class ItemContent(BaseModel):
    item_id: str
    message: str
    checked: bool


class AddItemRequest(ItemContent):
    ...


class DeleteItemRequest(BaseModel):
    item_id: str


class CheckItemRequest(BaseModel):
    item_id: str


class FetchItemsRequest(BaseModel):
    user_identifier: int


class FetchItemsResponse(BaseModel):
    items: "list[ItemContent]"


class OutcomeResponse(BaseModel):
    """
    Used for all responses but the fetch item request.
    Indicates whether the operation worked or not
    """

    success: bool
