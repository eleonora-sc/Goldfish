from typing import Any, Dict, List, Optional, Unpack, Required, Optional, TypedDict, Union, NotRequired,overload


class GetMeasurementParams(TypedDict):
    sort: NotRequired[str]
    id__lt: NotRequired[str]
    id__lte: NotRequired[str]
    id__gt: NotRequired[str]
    id__gte: NotRequired[str]
    id__in: NotRequired[str]
    id: NotRequired[str]
    start_time: NotRequired[int]
    start_time__lt: NotRequired[int]
    start_time__lte: NotRequired[int]
    start_time__gt: NotRequired[int]
    start_time__gte: NotRequired[int]
    stop_time: NotRequired[int]
    stop_time__lt: NotRequired[int]
    stop_time__lte: NotRequired[int]
    stop_time__gt: NotRequired[int]
    stop_time__gte: NotRequired[int]
    is_public: NotRequired[bool]
    is_oneoff: NotRequired[bool]
    interval: NotRequired[str]
    interval__lt: NotRequired[str]
    interval__lte: NotRequired[str]
    interval__gt: NotRequired[str]
    interval__gte: NotRequired[str]
    status: NotRequired[str]
    status__in: NotRequired[str]
    tags: NotRequired[str]
    type: NotRequired[str]
    target_ip: NotRequired[str]
    current_probes: NotRequired[str]
    participant_logs_probes: NotRequired[str]
    target_asn: NotRequired[str]
    target: NotRequired[str]
    target__contains: NotRequired[str]
    target__startswith: NotRequired[str]
    target__endswith: NotRequired[str]
    description: NotRequired[str]
    description__contains: NotRequired[str]
    description__startswith: NotRequired[str]
    description__endswith: NotRequired[str]
    af: NotRequired[str]
    search: NotRequired[str]
    protocol: NotRequired[str]
    group_id: NotRequired[str]
    group: NotRequired[str]
    favourite: NotRequired[bool]
    hidden: NotRequired[bool]
    page: NotRequired[int]
    page_size: NotRequired[int]
    after: NotRequired[str]
    format: NotRequired[str]
    callback: NotRequired[str]
    optional_fields: NotRequired[str]
    fields: NotRequired[str]
    format_datetime: NotRequired[str]
    key: NotRequired[str]
    mine: NotRequired[bool]

class TracerouteParams(TypedDict):
    target: Required[str]
    description: Required[str]
    type: Required[str]
    af: Required[int]
    resolve_on_probe: NotRequired[bool]
    is_public: NotRequired[bool]
    packets: NotRequired[int]
    protocol: NotRequired[str]
    paris: NotRequired[int]
    firsthop: NotRequired[int]
    interval: NotRequired[int]
    is_oneoff: NotRequired[bool]

class PingParams(TypedDict):
    target: str
    description: str
    type: str
    af: int
    resolve_on_probe: NotRequired[bool]
    is_public: NotRequired[bool]

class GetProbeParams(TypedDict):
    pass

class GetMeasurementParams(TypedDict):
    pass

class ProbeParams(TypedDict):
    requested: int
    type: str
    value: Union[str,int]