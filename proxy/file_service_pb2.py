"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 6, 31, 1, "", "file_service.proto"
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x12\x66ile_service.proto\x12\x0c\x66iletransfer"E\n\x11\x46ileUploadRequest\x12\x12\n\x08\x66ilename\x18\x01 \x01(\tH\x00\x12\x14\n\nchunk_data\x18\x02 \x01(\x0cH\x00\x42\x06\n\x04\x64\x61ta"3\n\x12\x46ileUploadResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0c\n\x04size\x18\x02 \x01(\x05\x32`\n\x0b\x46ileService\x12Q\n\nUploadFile\x12\x1f.filetransfer.FileUploadRequest\x1a .filetransfer.FileUploadResponse(\x01\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "file_service_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_FILEUPLOADREQUEST"]._serialized_start = 36
    _globals["_FILEUPLOADREQUEST"]._serialized_end = 105
    _globals["_FILEUPLOADRESPONSE"]._serialized_start = 107
    _globals["_FILEUPLOADRESPONSE"]._serialized_end = 158
    _globals["_FILESERVICE"]._serialized_start = 160
    _globals["_FILESERVICE"]._serialized_end = 256
# @@protoc_insertion_point(module_scope)
