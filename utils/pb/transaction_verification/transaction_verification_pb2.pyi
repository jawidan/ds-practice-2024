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

class VectorClock(_message.Message):
    __slots__ = ("timestamps",)
    class TimestampsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    TIMESTAMPS_FIELD_NUMBER: _ClassVar[int]
    timestamps: _containers.ScalarMap[str, int]
    def __init__(self, timestamps: _Optional[_Mapping[str, int]] = ...) -> None: ...

class CreditCard(_message.Message):
    __slots__ = ("number", "expirationDate", "cvv")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONDATE_FIELD_NUMBER: _ClassVar[int]
    CVV_FIELD_NUMBER: _ClassVar[int]
    number: str
    expirationDate: str
    cvv: str
    def __init__(self, number: _Optional[str] = ..., expirationDate: _Optional[str] = ..., cvv: _Optional[str] = ...) -> None: ...

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

class TransactionVerificationRequest(_message.Message):
    __slots__ = ("user", "creditCard", "items", "billingAddress", "termsAndConditionsAccepted", "vector_clock")
    USER_FIELD_NUMBER: _ClassVar[int]
    CREDITCARD_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    BILLINGADDRESS_FIELD_NUMBER: _ClassVar[int]
    TERMSANDCONDITIONSACCEPTED_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    user: User
    creditCard: CreditCard
    items: _containers.RepeatedCompositeFieldContainer[Item]
    billingAddress: BillingAddress
    termsAndConditionsAccepted: bool
    vector_clock: VectorClock
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., creditCard: _Optional[_Union[CreditCard, _Mapping]] = ..., items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ..., billingAddress: _Optional[_Union[BillingAddress, _Mapping]] = ..., termsAndConditionsAccepted: bool = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class TransactionVerificationResponse(_message.Message):
    __slots__ = ("verification", "errors", "vector_clock")
    VERIFICATION_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    verification: bool
    errors: _containers.RepeatedScalarFieldContainer[str]
    vector_clock: VectorClock
    def __init__(self, verification: bool = ..., errors: _Optional[_Iterable[str]] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...
