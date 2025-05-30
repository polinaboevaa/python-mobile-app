# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: schedule.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'schedule.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eschedule.proto\x12\x12\x61pp.grpc.generated\"s\n\rScheduleModel\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x10\n\x08medicine\x18\x02 \x01(\t\x12\x11\n\tfrequency\x18\x03 \x01(\x05\x12\x1a\n\rduration_days\x18\x04 \x01(\x05H\x00\x88\x01\x01\x42\x10\n\x0e_duration_days\" \n\rUserIdRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\"5\n\rScheduleQuery\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x13\n\x0bschedule_id\x18\x02 \x01(\x05\"&\n\x0fScheduleIdModel\x12\x13\n\x0bschedule_id\x18\x01 \x01(\x05\"4\n\x15SchedulesListResponse\x12\x1b\n\x13\x61\x63tive_schedule_ids\x18\x01 \x03(\x05\"P\n\x14\x46ullScheduleResponse\x12\x13\n\x0bschedule_id\x18\x01 \x01(\x05\x12\x10\n\x08medicine\x18\x02 \x01(\t\x12\x11\n\ttime_list\x18\x03 \x03(\t\"\"\n\x0fMessageResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1f\n\rErrorResponse\x12\x0e\n\x06\x64\x65tail\x18\x01 \x01(\t\"\x89\x01\n\x10ScheduleResponse\x12?\n\rfull_schedule\x18\x01 \x01(\x0b\x32(.app.grpc.generated.FullScheduleResponse\x12\x34\n\x07message\x18\x02 \x01(\x0b\x32#.app.grpc.generated.MessageResponse\"\xd8\x01\n\x18\x44ynamicSchedulesResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12W\n\x0eschedule_times\x18\x02 \x03(\x0b\x32?.app.grpc.generated.DynamicSchedulesResponse.ScheduleTimesEntry\x1aR\n\x12ScheduleTimesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12+\n\x05value\x18\x02 \x01(\x0b\x32\x1c.app.grpc.generated.TimeList:\x02\x38\x01\"\x19\n\x08TimeList\x12\r\n\x05times\x18\x01 \x03(\t2\x85\x03\n\x0fScheduleService\x12U\n\x0b\x41\x64\x64Schedule\x12!.app.grpc.generated.ScheduleModel\x1a#.app.grpc.generated.ScheduleIdModel\x12\\\n\x0cGetSchedules\x12!.app.grpc.generated.UserIdRequest\x1a).app.grpc.generated.SchedulesListResponse\x12Z\n\x0fGetScheduleById\x12!.app.grpc.generated.ScheduleQuery\x1a$.app.grpc.generated.ScheduleResponse\x12\x61\n\x0eGetNextTakings\x12!.app.grpc.generated.UserIdRequest\x1a,.app.grpc.generated.DynamicSchedulesResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'schedule_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_DYNAMICSCHEDULESRESPONSE_SCHEDULETIMESENTRY']._loaded_options = None
  _globals['_DYNAMICSCHEDULESRESPONSE_SCHEDULETIMESENTRY']._serialized_options = b'8\001'
  _globals['_SCHEDULEMODEL']._serialized_start=38
  _globals['_SCHEDULEMODEL']._serialized_end=153
  _globals['_USERIDREQUEST']._serialized_start=155
  _globals['_USERIDREQUEST']._serialized_end=187
  _globals['_SCHEDULEQUERY']._serialized_start=189
  _globals['_SCHEDULEQUERY']._serialized_end=242
  _globals['_SCHEDULEIDMODEL']._serialized_start=244
  _globals['_SCHEDULEIDMODEL']._serialized_end=282
  _globals['_SCHEDULESLISTRESPONSE']._serialized_start=284
  _globals['_SCHEDULESLISTRESPONSE']._serialized_end=336
  _globals['_FULLSCHEDULERESPONSE']._serialized_start=338
  _globals['_FULLSCHEDULERESPONSE']._serialized_end=418
  _globals['_MESSAGERESPONSE']._serialized_start=420
  _globals['_MESSAGERESPONSE']._serialized_end=454
  _globals['_ERRORRESPONSE']._serialized_start=456
  _globals['_ERRORRESPONSE']._serialized_end=487
  _globals['_SCHEDULERESPONSE']._serialized_start=490
  _globals['_SCHEDULERESPONSE']._serialized_end=627
  _globals['_DYNAMICSCHEDULESRESPONSE']._serialized_start=630
  _globals['_DYNAMICSCHEDULESRESPONSE']._serialized_end=846
  _globals['_DYNAMICSCHEDULESRESPONSE_SCHEDULETIMESENTRY']._serialized_start=764
  _globals['_DYNAMICSCHEDULESRESPONSE_SCHEDULETIMESENTRY']._serialized_end=846
  _globals['_TIMELIST']._serialized_start=848
  _globals['_TIMELIST']._serialized_end=873
  _globals['_SCHEDULESERVICE']._serialized_start=876
  _globals['_SCHEDULESERVICE']._serialized_end=1265
# @@protoc_insertion_point(module_scope)
