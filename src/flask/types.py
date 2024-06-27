from pydantic import BaseModel  # type: ignore


class AddItemRequest(BaseModel):
    item_id: str
    message: str


class DeleteItemRequest(BaseModel):
    item_id: str


class CheckItemRequest(BaseModel):
    is_checked: bool


class FetchItemsRequest(BaseModel):
    user_identifier: int


class FetchItemsResponse(BaseModel):
    item_id: str
    message: str


class OutcomeResponse(BaseModel):
    """
    Used for all responses but the fetch item request.
    Indicates whether the operation worked or not
    """

    success: bool
