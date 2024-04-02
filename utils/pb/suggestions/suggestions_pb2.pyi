from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

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

class BookRequest(_message.Message):
    __slots__ = ("name", "vector_clock")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    name: str
    vector_clock: VectorClock
    def __init__(self, name: _Optional[str] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...

class BookResponse(_message.Message):
    __slots__ = ("name", "vector_clock")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VECTOR_CLOCK_FIELD_NUMBER: _ClassVar[int]
    name: str
    vector_clock: VectorClock
    def __init__(self, name: _Optional[str] = ..., vector_clock: _Optional[_Union[VectorClock, _Mapping]] = ...) -> None: ...
