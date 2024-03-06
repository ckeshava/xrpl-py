"""Models for the Ledger Object `RippleState`"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, cast

from xrpl.models.amounts.issued_currency_amount import IssuedCurrencyAmount
from xrpl.models.flags import FlagInterface
from xrpl.models.ledger_objects.ledger_entry_type import LedgerEntryType
from xrpl.models.ledger_objects.ledger_object import HasPreviousTxnID, LedgerObject
from xrpl.models.required import REQUIRED
from xrpl.models.utils import isFlagEnabled, require_kwargs_on_init


@require_kwargs_on_init
@dataclass(frozen=True)
class RippleState(LedgerObject, HasPreviousTxnID):
    """The model for the `RippleState` Ledger Object"""

    balance: IssuedCurrencyAmount = REQUIRED  # type: ignore
    """
    The balance of the trust line, from the perspective of the low account. A negative
    balance indicates that the high account holds tokens issued by the low account. The
    issuer in this is always set to the neutral value ACCOUNT_ONE. This field is
    required.
    """

    high_limit: IssuedCurrencyAmount = REQUIRED  # type: ignore
    """
    The limit that the high account has set on the trust line. The `issuer` is the
    address of the high account that set this limit. This field is required.
    """

    low_limit: IssuedCurrencyAmount = REQUIRED  # type: ignore
    """
    The limit that the low account has set on the trust line. The `issuer` is the
    address of the low account that set this limit. This field is required.
    """

    high_node: Optional[str] = None
    """
    (Omitted in some historical ledgers) A hint indicating which page of the high
    account's owner directory links to this entry, in case the directory consists of
    multiple pages.
    """

    high_quality_in: Optional[int] = None
    """
    The inbound quality set by the high account, as an integer in the implied ratio
    `HighQualityIn`:1,000,000,000. As a special case, the value 0 is equivalent to 1
    billion, or face value.
    """

    high_quality_out: Optional[int] = None
    """
    The outbound quality set by the high account, as an integer in the implied ratio
    `HighQualityOut`:1,000,000,000. As a special case, the value 0 is equivalent to 1
    billion, or face value.
    """

    low_node: Optional[str] = None
    """
    (Omitted in some historical ledgers) A hint indicating which page of the low
    account's owner directory links to this entry, in case the directory consists of
    multiple pages.
    """

    low_quality_in: Optional[int] = None
    """
    The inbound quality set by the low account, as an integer in the implied ratio
    `LowQualityIn`:1,000,000,000. As a special case, the value 0 is equivalent to 1
    billion, or face value.
    """

    low_quality_out: Optional[int] = None
    """
    The outbound quality set by the low account, as an integer in the implied ratio
    `LowQualityOut`:1,000,000,000. As a special case, the value 0 is equivalent to 1
    billion, or face value.
    """

    ledger_entry_type: LedgerEntryType = field(
        default=LedgerEntryType.RIPPLE_STATE,
        init=False,
    )


class RippleStateFlag(Enum):
    """The flags for the `RippleState` Ledger Object"""

    LSF_LOW_RESERVE = 0x00010000
    LSF_HIGH_RESERVE = 0x00020000
    LSF_LOW_AUTH = 0x00040000
    LSF_HIGH_AUTH = 0x00080000
    LSF_LOW_NO_RIPPLE = 0x00100000
    LSF_HIGH_NO_RIPPLE = 0x00200000
    LSF_LOW_FREEZE = 0x00400000
    LSF_HIGH_FREEZE = 0x00800000


class RippleStateFlagsInterface(FlagInterface):
    """This is used to indicate the presence of certain flags in the RippleState Ledger
    Object
    """

    LSF_LOW_RESERVE: bool
    LSF_HIGH_RESERVE: bool
    LSF_LOW_AUTH: bool
    LSF_HIGH_AUTH: bool
    LSF_LOW_NO_RIPPLE: bool
    LSF_HIGH_NO_RIPPLE: bool
    LSF_LOW_FREEZE: bool
    LSF_HIGH_FREEZE: bool


def parseRippleStateFlags(flags: int) -> RippleStateFlagsInterface:
    """
    Parses integer flag input into a FlagsInterface object

    Args:
        flags: Input flags are represented as an integer

    Returns:
        RippleStateFlagsInterface object is returned

    """
    # flags_interface will be cast into a RippleStateFlagsInterface at the end
    # A Dictionary is used instead of a TypedDict because the former allows arbitrary
    # string indexes. This is useful to traverse across RippleStateFlag enum
    flags_interface = {}

    for flag in RippleStateFlag:
        flags_interface[flag.name] = isFlagEnabled(flags, flag.value)
    return cast(RippleStateFlagsInterface, flags_interface)
