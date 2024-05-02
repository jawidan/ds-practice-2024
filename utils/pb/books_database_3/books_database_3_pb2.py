# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: books_database_3/books_database_3.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'books_database_3/books_database_3.proto\x12\x10\x62ooks_database_3\"%\n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontact\x18\x02 \x01(\t\"&\n\x04Item\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\"[\n\x0e\x42illingAddress\x12\x0e\n\x06street\x18\x01 \x01(\t\x12\x0c\n\x04\x63ity\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\x12\x0b\n\x03zip\x18\x04 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x05 \x01(\t\"\x9b\x01\n\x12\x43reateOrderRequest\x12$\n\x04user\x18\x01 \x01(\x0b\x32\x16.books_database_3.User\x12%\n\x05items\x18\x02 \x03(\x0b\x32\x16.books_database_3.Item\x12\x38\n\x0e\x62illingAddress\x18\x03 \x01(\x0b\x32 .books_database_3.BillingAddress\">\n\x13\x43reateOrderResponse\x12\x0f\n\x02id\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x0f\n\x07success\x18\x02 \x01(\x08\x42\x05\n\x03_id\"\x9c\x01\n\x13PrepareOrderRequest\x12$\n\x04user\x18\x01 \x01(\x0b\x32\x16.books_database_3.User\x12%\n\x05items\x18\x02 \x03(\x0b\x32\x16.books_database_3.Item\x12\x38\n\x0e\x62illingAddress\x18\x03 \x01(\x0b\x32 .books_database_3.BillingAddress\"\'\n\x14PrepareOrderResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x9e\x01\n\x11\x43reateBookRequest\x12\r\n\x05title\x18\x01 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0e\n\x06\x63opies\x18\x04 \x01(\t\x12\x17\n\x0f\x63opiesAvailable\x18\x05 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x06 \x01(\t\x12\x0b\n\x03img\x18\x07 \x01(\t\x12\r\n\x05price\x18\x08 \x01(\x05\" \n\x12\x43reateBookResponse\x12\n\n\x02id\x18\x01 \x01(\x05\"\x9d\x01\n\x04\x42ook\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x04 \x01(\t\x12\x0e\n\x06\x63opies\x18\x05 \x01(\t\x12\x17\n\x0f\x63opiesAvailable\x18\x06 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x07 \x01(\t\x12\x0b\n\x03img\x18\x08 \x01(\t\x12\r\n\x05price\x18\t \x01(\x05\"\x11\n\x0fGetBooksRequest\"9\n\x10GetBooksResponse\x12%\n\x05\x62ooks\x18\x01 \x03(\x0b\x32\x16.books_database_3.Book2\xc9\x01\n\x0cOrderService\x12Z\n\x0b\x43reateOrder\x12$.books_database_3.CreateOrderRequest\x1a%.books_database_3.CreateOrderResponse\x12]\n\x0cPrepareOrder\x12%.books_database_3.PrepareOrderRequest\x1a&.books_database_3.PrepareOrderResponse2\xb9\x01\n\x0b\x42ookService\x12W\n\nCreateBook\x12#.books_database_3.CreateBookRequest\x1a$.books_database_3.CreateBookResponse\x12Q\n\x08GetBooks\x12!.books_database_3.GetBooksRequest\x1a\".books_database_3.GetBooksResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'books_database_3.books_database_3_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_USER']._serialized_start=61
  _globals['_USER']._serialized_end=98
  _globals['_ITEM']._serialized_start=100
  _globals['_ITEM']._serialized_end=138
  _globals['_BILLINGADDRESS']._serialized_start=140
  _globals['_BILLINGADDRESS']._serialized_end=231
  _globals['_CREATEORDERREQUEST']._serialized_start=234
  _globals['_CREATEORDERREQUEST']._serialized_end=389
  _globals['_CREATEORDERRESPONSE']._serialized_start=391
  _globals['_CREATEORDERRESPONSE']._serialized_end=453
  _globals['_PREPAREORDERREQUEST']._serialized_start=456
  _globals['_PREPAREORDERREQUEST']._serialized_end=612
  _globals['_PREPAREORDERRESPONSE']._serialized_start=614
  _globals['_PREPAREORDERRESPONSE']._serialized_end=653
  _globals['_CREATEBOOKREQUEST']._serialized_start=656
  _globals['_CREATEBOOKREQUEST']._serialized_end=814
  _globals['_CREATEBOOKRESPONSE']._serialized_start=816
  _globals['_CREATEBOOKRESPONSE']._serialized_end=848
  _globals['_BOOK']._serialized_start=851
  _globals['_BOOK']._serialized_end=1008
  _globals['_GETBOOKSREQUEST']._serialized_start=1010
  _globals['_GETBOOKSREQUEST']._serialized_end=1027
  _globals['_GETBOOKSRESPONSE']._serialized_start=1029
  _globals['_GETBOOKSRESPONSE']._serialized_end=1086
  _globals['_ORDERSERVICE']._serialized_start=1089
  _globals['_ORDERSERVICE']._serialized_end=1290
  _globals['_BOOKSERVICE']._serialized_start=1293
  _globals['_BOOKSERVICE']._serialized_end=1478
# @@protoc_insertion_point(module_scope)
