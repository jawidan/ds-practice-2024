# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: order_executor/order_executor.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#order_executor/order_executor.proto\x12\rorderexecutor\"\x10\n\x0e\x44\x65queueRequest\"\"\n\x0f\x44\x65queueResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2e\n\x14OrderExecutorService\x12M\n\x0c\x44\x65queueOrder\x12\x1d.orderexecutor.DequeueRequest\x1a\x1e.orderexecutor.DequeueResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_executor.order_executor_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_DEQUEUEREQUEST']._serialized_start=54
  _globals['_DEQUEUEREQUEST']._serialized_end=70
  _globals['_DEQUEUERESPONSE']._serialized_start=72
  _globals['_DEQUEUERESPONSE']._serialized_end=106
  _globals['_ORDEREXECUTORSERVICE']._serialized_start=108
  _globals['_ORDEREXECUTORSERVICE']._serialized_end=209
# @@protoc_insertion_point(module_scope)
