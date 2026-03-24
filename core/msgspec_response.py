"""Msgspec integration for Litestar - JSON serialization of Struct types."""

from typing import Any

import msgspec
from litestar.response import Response


class MsgspecJSONResponse(Response):
    """Custom Response class that serializes msgspec.Struct types."""

    def __init__(self, content: Any, **kwargs):
        # Encode content using msgspec JSON encoder
        encoded = msgspec.json.encode(content)
        super().__init__(
            content=encoded,
            media_type="application/json",
            **kwargs,
        )


def msgspec_json_response_handler(data: Any) -> MsgspecJSONResponse:
    """Default response handler for msgspec data."""
    return MsgspecJSONResponse(data)
