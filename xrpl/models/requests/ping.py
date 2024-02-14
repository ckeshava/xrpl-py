"""
The ping command returns an acknowledgement, so that
clients can test the connection status and latency.
"""
from dataclasses import dataclass, field

from xrpl.models.requests.request import Request, RequestMethod
from xrpl.models.utils import KW_ONLY_DATACLASS


@dataclass(frozen=True, **KW_ONLY_DATACLASS)
class Ping(Request):
    """
    The ping command returns an acknowledgement, so that
    clients can test the connection status and latency.
    """

    method: RequestMethod = field(default=RequestMethod.PING, init=False)
