# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yandex.protoc
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""

try:
    from google.protobuf import descriptor as _descriptor
except:
    import os
    import sys

    sys.path.append(
        os.path.dirname(os.path.abspath(__file__)) + "\\..\\protobuf-4.25.2-py3-none-any.whl.pypi",
    )

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\ryandex.protoc"?\n\x1aVideoTranslationHelpObject\x12\x0e\n\x06target\x18\x01 \x01(\t\x12\x11\n\ttargetUrl\x18\x02 \x01(\t"\x8a\x02\n\x17VideoTranslationRequest\x12\x0b\n\x03url\x18\x03 \x01(\t\x12\x10\n\x08\x64\x65viceId\x18\x04 \x01(\t\x12\x14\n\x0c\x66irstRequest\x18\x05 \x01(\x08\x12\x10\n\x08\x64uration\x18\x06 \x01(\x01\x12\x10\n\x08unknown2\x18\x07 \x01(\x05\x12\x10\n\x08language\x18\x08 \x01(\t\x12\x10\n\x08unknown3\x18\t \x01(\x05\x12\x10\n\x08unknown4\x18\n \x01(\x05\x12\x34\n\x0ftranslationHelp\x18\x0b \x03(\x0b\x32\x1b.VideoTranslationHelpObject\x12\x18\n\x10responseLanguage\x18\x0e \x01(\t\x12\x10\n\x08unknown5\x18\x0f \x01(\x05"6\n\x15VideoSubtitlesRequest\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x10\n\x08language\x18\x02 \x01(\t"M\n\x12VideoStreamRequest\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x10\n\x08language\x18\x02 \x01(\t\x12\x18\n\x10responseLanguage\x18\x03 \x01(\t"(\n\x16VideoStreamPingRequest\x12\x0e\n\x06pingId\x18\x01 \x01(\x05"\xa6\x01\n\x18VideoTranslationResponse\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x10\n\x08\x64uration\x18\x02 \x01(\x01\x12\x0e\n\x06status\x18\x04 \x01(\x05\x12\x15\n\rremainingTime\x18\x05 \x01(\x05\x12\x10\n\x08unknown0\x18\x06 \x01(\x05\x12\x0f\n\x07\x65rrcode\x18\x07 \x01(\t\x12\x10\n\x08language\x18\x08 \x01(\t\x12\x0f\n\x07message\x18\t \x01(\x0c"\x9e\x01\n\x14VideoSubtitlesObject\x12\x10\n\x08language\x18\x01 \x01(\t\x12\x0b\n\x03url\x18\x02 \x01(\t\x12\x10\n\x08unknown2\x18\x03 \x01(\x05\x12\x1a\n\x12translatedLanguage\x18\x04 \x01(\t\x12\x15\n\rtranslatedUrl\x18\x05 \x01(\t\x12\x10\n\x08unknown5\x18\x06 \x01(\x05\x12\x10\n\x08unknown6\x18\x07 \x01(\x05"T\n\x16VideoSubtitlesResponse\x12\x10\n\x08unknown0\x18\x01 \x01(\x05\x12(\n\tsubtitles\x18\x02 \x03(\x0b\x32\x15.VideoSubtitlesObject"3\n\x11VideoStreamObject\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x03"c\n\x13VideoStreamResponse\x12\x10\n\x08interval\x18\x01 \x01(\x05\x12*\n\x0etranslatedInfo\x18\x02 \x01(\x0b\x32\x12.VideoStreamObject\x12\x0e\n\x06pingId\x18\x03 \x01(\x05"<\n\x1bVideoWhitelistStreamRequest\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x10\n\x08\x64\x65viceId\x18\x04 \x01(\t"3\n\x1cVideoWhitelistStreamResponse\x12\x13\n\x0binWhitelist\x18\x01 \x01(\x08',
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "yandex_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_VIDEOTRANSLATIONHELPOBJECT"]._serialized_start = 17
    _globals["_VIDEOTRANSLATIONHELPOBJECT"]._serialized_end = 80
    _globals["_VIDEOTRANSLATIONREQUEST"]._serialized_start = 83
    _globals["_VIDEOTRANSLATIONREQUEST"]._serialized_end = 349
    _globals["_VIDEOSUBTITLESREQUEST"]._serialized_start = 351
    _globals["_VIDEOSUBTITLESREQUEST"]._serialized_end = 405
    _globals["_VIDEOSTREAMREQUEST"]._serialized_start = 407
    _globals["_VIDEOSTREAMREQUEST"]._serialized_end = 484
    _globals["_VIDEOSTREAMPINGREQUEST"]._serialized_start = 486
    _globals["_VIDEOSTREAMPINGREQUEST"]._serialized_end = 526
    _globals["_VIDEOTRANSLATIONRESPONSE"]._serialized_start = 529
    _globals["_VIDEOTRANSLATIONRESPONSE"]._serialized_end = 695
    _globals["_VIDEOSUBTITLESOBJECT"]._serialized_start = 698
    _globals["_VIDEOSUBTITLESOBJECT"]._serialized_end = 856
    _globals["_VIDEOSUBTITLESRESPONSE"]._serialized_start = 858
    _globals["_VIDEOSUBTITLESRESPONSE"]._serialized_end = 942
    _globals["_VIDEOSTREAMOBJECT"]._serialized_start = 944
    _globals["_VIDEOSTREAMOBJECT"]._serialized_end = 995
    _globals["_VIDEOSTREAMRESPONSE"]._serialized_start = 997
    _globals["_VIDEOSTREAMRESPONSE"]._serialized_end = 1096
    _globals["_VIDEOWHITELISTSTREAMREQUEST"]._serialized_start = 1098
    _globals["_VIDEOWHITELISTSTREAMREQUEST"]._serialized_end = 1158
    _globals["_VIDEOWHITELISTSTREAMRESPONSE"]._serialized_start = 1160
    _globals["_VIDEOWHITELISTSTREAMRESPONSE"]._serialized_end = 1211
# @@protoc_insertion_point(module_scope)
