# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: suggestions/suggestions.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dsuggestions/suggestions.proto\x12\x0bsuggestions\"\x1b\n\x0b\x42ookRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x1c\n\x0c\x42ookResponse\x12\x0c\n\x04name\x18\x01 \x01(\t2\\\n\x15\x42ookSuggestionService\x12\x43\n\x0cSuggestBooks\x12\x18.suggestions.BookRequest\x1a\x19.suggestions.BookResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'suggestions.suggestions_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_BOOKREQUEST']._serialized_start=46
  _globals['_BOOKREQUEST']._serialized_end=73
  _globals['_BOOKRESPONSE']._serialized_start=75
  _globals['_BOOKRESPONSE']._serialized_end=103
  _globals['_BOOKSUGGESTIONSERVICE']._serialized_start=105
  _globals['_BOOKSUGGESTIONSERVICE']._serialized_end=197
# @@protoc_insertion_point(module_scope)
