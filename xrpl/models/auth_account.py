"""Model used in AMMBid transaction."""
from __future__ import annotations

from dataclasses import dataclass

from xrpl.models.nested_model import NestedModel
from xrpl.models.required import REQUIRED
from xrpl.models.utils import KW_ONLY_DATACLASS


@dataclass(frozen=True, **KW_ONLY_DATACLASS)
class AuthAccount(NestedModel):
    """Represents one entry in a list of AuthAccounts used in AMMBid transaction."""

    account: str = REQUIRED  # type: ignore
    """
    This field is required.

    :meta hide-value:
    """
