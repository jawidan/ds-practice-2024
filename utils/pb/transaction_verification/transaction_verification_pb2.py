# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transaction_verification/transaction_verification.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n7transaction_verification/transaction_verification.proto\x12\x0btransaction\"%\n\x04User\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontact\x18\x02 \x01(\t\"~\n\x0bVectorClock\x12<\n\ntimestamps\x18\x01 \x03(\x0b\x32(.transaction.VectorClock.TimestampsEntry\x1a\x31\n\x0fTimestampsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\"A\n\nCreditCard\x12\x0e\n\x06number\x18\x01 \x01(\t\x12\x16\n\x0e\x65xpirationDate\x18\x02 \x01(\t\x12\x0b\n\x03\x63vv\x18\x03 \x01(\t\"&\n\x04Item\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\"[\n\x0e\x42illingAddress\x12\x0e\n\x06street\x18\x01 \x01(\t\x12\x0c\n\x04\x63ity\x18\x02 \x01(\t\x12\r\n\x05state\x18\x03 \x01(\t\x12\x0b\n\x03zip\x18\x04 \x01(\t\x12\x0f\n\x07\x63ountry\x18\x05 \x01(\t\"\x99\x02\n\x1eTransactionVerificationRequest\x12\x1f\n\x04user\x18\x01 \x01(\x0b\x32\x11.transaction.User\x12+\n\ncreditCard\x18\x02 \x01(\x0b\x32\x17.transaction.CreditCard\x12 \n\x05items\x18\x03 \x03(\x0b\x32\x11.transaction.Item\x12\x33\n\x0e\x62illingAddress\x18\x04 \x01(\x0b\x32\x1b.transaction.BillingAddress\x12\"\n\x1atermsAndConditionsAccepted\x18\x05 \x01(\x08\x12.\n\x0cvector_clock\x18\x06 \x01(\x0b\x32\x18.transaction.VectorClock\"w\n\x1fTransactionVerificationResponse\x12\x14\n\x0cverification\x18\x01 \x01(\x08\x12\x0e\n\x06\x65rrors\x18\x02 \x03(\t\x12.\n\x0cvector_clock\x18\x03 \x01(\x0b\x32\x18.transaction.VectorClock2\x90\x01\n\x1eTransactionVerificationService\x12n\n\x11VerifyTransaction\x12+.transaction.TransactionVerificationRequest\x1a,.transaction.TransactionVerificationResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_verification.transaction_verification_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_VECTORCLOCK_TIMESTAMPSENTRY']._options = None
  _globals['_VECTORCLOCK_TIMESTAMPSENTRY']._serialized_options = b'8\001'
  _globals['_USER']._serialized_start=72
  _globals['_USER']._serialized_end=109
  _globals['_VECTORCLOCK']._serialized_start=111
  _globals['_VECTORCLOCK']._serialized_end=237
  _globals['_VECTORCLOCK_TIMESTAMPSENTRY']._serialized_start=188
  _globals['_VECTORCLOCK_TIMESTAMPSENTRY']._serialized_end=237
  _globals['_CREDITCARD']._serialized_start=239
  _globals['_CREDITCARD']._serialized_end=304
  _globals['_ITEM']._serialized_start=306
  _globals['_ITEM']._serialized_end=344
  _globals['_BILLINGADDRESS']._serialized_start=346
  _globals['_BILLINGADDRESS']._serialized_end=437
  _globals['_TRANSACTIONVERIFICATIONREQUEST']._serialized_start=440
  _globals['_TRANSACTIONVERIFICATIONREQUEST']._serialized_end=721
  _globals['_TRANSACTIONVERIFICATIONRESPONSE']._serialized_start=723
  _globals['_TRANSACTIONVERIFICATIONRESPONSE']._serialized_end=842
  _globals['_TRANSACTIONVERIFICATIONSERVICE']._serialized_start=845
  _globals['_TRANSACTIONVERIFICATIONSERVICE']._serialized_end=989
# @@protoc_insertion_point(module_scope)
