from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("name", "contact")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    name: str
    contact: str
    def __init__(self, name: _Optional[str] = ..., contact: _Optional[str] = ...) -> None: ...

class Item(_message.Message):
    __slots__ = ("name", "quantity")
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    name: str
    quantity: int
    def __init__(self, name: _Optional[str] = ..., quantity: _Optional[int] = ...) -> None: ...

class BillingAddress(_message.Message):
    __slots__ = ("street", "city", "state", "zip", "country")
    STREET_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ZIP_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    street: str
    city: str
    state: str
    zip: str
    country: str
    def __init__(self, street: _Optional[str] = ..., city: _Optional[str] = ..., state: _Optional[str] = ..., zip: _Optional[str] = ..., country: _Optional[str] = ...) -> None: ...

class CreateOrderRequest(_message.Message):
    __slots__ = ("user", "items", "billingAddress")
    USER_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    BILLINGADDRESS_FIELD_NUMBER: _ClassVar[int]
    user: User
    items: _containers.RepeatedCompositeFieldContainer[Item]
    billingAddress: BillingAddress
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ..., billingAddress: _Optional[_Union[BillingAddress, _Mapping]] = ...) -> None: ...

class CreateOrderResponse(_message.Message):
    __slots__ = ("id", "success")
    ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    id: int
    success: bool
    def __init__(self, id: _Optional[int] = ..., success: bool = ...) -> None: ...

class PrepareOrderRequest(_message.Message):
    __slots__ = ("user", "items", "billingAddress")
    USER_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    BILLINGADDRESS_FIELD_NUMBER: _ClassVar[int]
    user: User
    items: _containers.RepeatedCompositeFieldContainer[Item]
    billingAddress: BillingAddress
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ..., billingAddress: _Optional[_Union[BillingAddress, _Mapping]] = ...) -> None: ...

class PrepareOrderResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class CreateBookRequest(_message.Message):
    __slots__ = ("title", "author", "description", "copies", "copiesAvailable", "category", "img", "price")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COPIES_FIELD_NUMBER: _ClassVar[int]
    COPIESAVAILABLE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    IMG_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    title: str
    author: str
    description: str
    copies: str
    copiesAvailable: str
    category: str
    img: str
    price: int
    def __init__(self, title: _Optional[str] = ..., author: _Optional[str] = ..., description: _Optional[str] = ..., copies: _Optional[str] = ..., copiesAvailable: _Optional[str] = ..., category: _Optional[str] = ..., img: _Optional[str] = ..., price: _Optional[int] = ...) -> None: ...

class CreateBookResponse(_message.Message):
    __slots__ = ("id", "success")
    ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    id: int
    success: bool
    def __init__(self, id: _Optional[int] = ..., success: bool = ...) -> None: ...

class Book(_message.Message):
    __slots__ = ("id", "title", "author", "description", "copies", "copiesAvailable", "category", "img", "price")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COPIES_FIELD_NUMBER: _ClassVar[int]
    COPIESAVAILABLE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    IMG_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    author: str
    description: str
    copies: str
    copiesAvailable: str
    category: str
    img: str
    price: int
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., author: _Optional[str] = ..., description: _Optional[str] = ..., copies: _Optional[str] = ..., copiesAvailable: _Optional[str] = ..., category: _Optional[str] = ..., img: _Optional[str] = ..., price: _Optional[int] = ...) -> None: ...

class GetBooksRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetBooksResponse(_message.Message):
    __slots__ = ("books",)
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    books: _containers.RepeatedCompositeFieldContainer[Book]
    def __init__(self, books: _Optional[_Iterable[_Union[Book, _Mapping]]] = ...) -> None: ...
