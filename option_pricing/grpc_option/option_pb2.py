# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: option.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='option.proto',
  package='',
  syntax='proto3',
  serialized_options=b'Z\010.;option',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0coption.proto\"\xd0\x01\n\x0e\x43omputeRequest\x12\x10\n\x08maxPrice\x18\x01 \x01(\x01\x12\x12\n\nvolatility\x18\x02 \x01(\x01\x12\t\n\x01r\x18\x03 \x01(\x01\x12\x0c\n\x04tMax\x18\x04 \x01(\x01\x12\x13\n\x0bstrikePrice\x18\x05 \x01(\x01\x12\x17\n\x0f\x63\x61lculationType\x18\x06 \x01(\t\x12\x0c\n\x04\x62\x65ta\x18\x07 \x01(\x01\x12\x12\n\nstartPrice\x18\x08 \x01(\x01\x12\x18\n\x10maturityTimeDays\x18\t \x01(\x05\x12\x15\n\rexpectedPrice\x18\n \x01(\x01\"\x92\x01\n\x08UxtSlice\x12\x0f\n\x01U\x18\x01 \x03(\x0b\x32\x04.Uxt\x12\x1d\n\x15\x43\x61lculatedOptionprice\x18\x02 \x01(\x01\x12 \n\x18\x43\x61lculatedExpirationDays\x18\x03 \x01(\x05\x12\x1c\n\x14\x43\x61lculatedAssetPrice\x18\x04 \x01(\x01\x12\x16\n\x0e\x43\x61lculatedBeta\x18\x05 \x01(\x01\"\x11\n\x03Uxt\x12\n\n\x02Ut\x18\x01 \x03(\x01\x32=\n\rOptionPricing\x12,\n\x0c\x43omputePrice\x12\x0f.ComputeRequest\x1a\t.UxtSlice\"\x00\x42\nZ\x08.;optionb\x06proto3'
)




_COMPUTEREQUEST = _descriptor.Descriptor(
  name='ComputeRequest',
  full_name='ComputeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='maxPrice', full_name='ComputeRequest.maxPrice', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='volatility', full_name='ComputeRequest.volatility', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='r', full_name='ComputeRequest.r', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tMax', full_name='ComputeRequest.tMax', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='strikePrice', full_name='ComputeRequest.strikePrice', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='calculationType', full_name='ComputeRequest.calculationType', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='beta', full_name='ComputeRequest.beta', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='startPrice', full_name='ComputeRequest.startPrice', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='maturityTimeDays', full_name='ComputeRequest.maturityTimeDays', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='expectedPrice', full_name='ComputeRequest.expectedPrice', index=9,
      number=10, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=225,
)


_UXTSLICE = _descriptor.Descriptor(
  name='UxtSlice',
  full_name='UxtSlice',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='U', full_name='UxtSlice.U', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='CalculatedOptionprice', full_name='UxtSlice.CalculatedOptionprice', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='CalculatedExpirationDays', full_name='UxtSlice.CalculatedExpirationDays', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='CalculatedAssetPrice', full_name='UxtSlice.CalculatedAssetPrice', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='CalculatedBeta', full_name='UxtSlice.CalculatedBeta', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=228,
  serialized_end=374,
)


_UXT = _descriptor.Descriptor(
  name='Uxt',
  full_name='Uxt',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Ut', full_name='Uxt.Ut', index=0,
      number=1, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=376,
  serialized_end=393,
)

_UXTSLICE.fields_by_name['U'].message_type = _UXT
DESCRIPTOR.message_types_by_name['ComputeRequest'] = _COMPUTEREQUEST
DESCRIPTOR.message_types_by_name['UxtSlice'] = _UXTSLICE
DESCRIPTOR.message_types_by_name['Uxt'] = _UXT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ComputeRequest = _reflection.GeneratedProtocolMessageType('ComputeRequest', (_message.Message,), {
  'DESCRIPTOR' : _COMPUTEREQUEST,
  '__module__' : 'option_pb2'
  # @@protoc_insertion_point(class_scope:ComputeRequest)
  })
_sym_db.RegisterMessage(ComputeRequest)

UxtSlice = _reflection.GeneratedProtocolMessageType('UxtSlice', (_message.Message,), {
  'DESCRIPTOR' : _UXTSLICE,
  '__module__' : 'option_pb2'
  # @@protoc_insertion_point(class_scope:UxtSlice)
  })
_sym_db.RegisterMessage(UxtSlice)

Uxt = _reflection.GeneratedProtocolMessageType('Uxt', (_message.Message,), {
  'DESCRIPTOR' : _UXT,
  '__module__' : 'option_pb2'
  # @@protoc_insertion_point(class_scope:Uxt)
  })
_sym_db.RegisterMessage(Uxt)


DESCRIPTOR._options = None

_OPTIONPRICING = _descriptor.ServiceDescriptor(
  name='OptionPricing',
  full_name='OptionPricing',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=395,
  serialized_end=456,
  methods=[
  _descriptor.MethodDescriptor(
    name='ComputePrice',
    full_name='OptionPricing.ComputePrice',
    index=0,
    containing_service=None,
    input_type=_COMPUTEREQUEST,
    output_type=_UXTSLICE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_OPTIONPRICING)

DESCRIPTOR.services_by_name['OptionPricing'] = _OPTIONPRICING

# @@protoc_insertion_point(module_scope)