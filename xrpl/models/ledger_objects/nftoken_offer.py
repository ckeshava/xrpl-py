"""Models for the Ledger Object `NFTokenOffer`"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, TypeVar, Union

from xrpl.models.base_model import BaseModel
from xrpl.models.flags import FlagInterface
from xrpl.models.ledger_objects.ledger_entry_type import LedgerEntryType
from xrpl.models.ledger_objects.ledger_object import HasPreviousTxnID, LedgerObject
from xrpl.models.required import REQUIRED
from xrpl.models.utils import require_kwargs_on_init

T = TypeVar("T")


@require_kwargs_on_init
@dataclass(frozen=True)
class NFTokenOffer(LedgerObject, HasPreviousTxnID):
    """The model for the `NFTokenOffer` Ledger Object"""

    amount: Union[str, NFToken] = REQUIRED  # type: ignore
    """
    Amount expected or offered for the NFToken. If the token has the `lsfOnlyXRP` flag
    set, the amount must be specified in XRP. Sell offers that specify assets other
    than XRP must specify a non-zero amount. Sell offers that specify XRP can be 'free'
    (that is, the Amount field can be equal to `"0"`). This field is required.
    """

    nftoken_id: str = REQUIRED  # type: ignore
    """
    The `NFTokenID` of the NFToken object referenced by this offer. This field is
    required.
    """

    owner: str = REQUIRED  # type: ignore
    """
    Owner of the account that is creating and owns the offer. Only the current Owner of
    an NFToken can create an offer to sell an NFToken, but any account can create an
    offer to buy an NFToken. This field is required.
    """

    destination: Optional[str] = None
    """
    The AccountID for which this offer is intended. If present, only that account can
    accept the offer.
    """

    expiration: Optional[int] = None
    """
    The time after which the offer is no longer active. The value is the number of
    seconds since the Ripple Epoch.
    """

    owner_node: str = REQUIRED  # type: ignore
    """
    Internal bookkeeping, indicating the page inside the owner directory where this
    token is being tracked. This field allows the efficient deletion of offers.
    """

    nftoken_offer_node: str = REQUIRED  # type: ignore
    """
    Internal bookkeeping, indicating the page inside the token buy or sell offer
    directory, as appropriate, where this token is being tracked. This field allows the
    efficient deletion of offers.
    """

    ledger_entry_type: LedgerEntryType = field(
        default=LedgerEntryType.NFTOKEN_OFFER,
        init=False,
    )


@require_kwargs_on_init
@dataclass(frozen=True)
class NFToken(BaseModel):  #
    """A model for the `NFToken` object"""

    nftoken_id: str = REQUIRED  # type: ignore
    uri: str = REQUIRED  # type: ignore


class NFTokenOfferFlags(Enum):
    """The flags for the `NFTokenOffer` Ledger Object"""

    LSF_SELL_NFTOKEN = 0x00000001


class NFTokenOfferFlagsInterface(FlagInterface):
    """The flags interface class for the `NFTokenOffer` Ledger Object"""

    LSF_SELL_NFTOKEN: bool
