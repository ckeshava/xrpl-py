"""The different ledger entry types"""

from enum import Enum


class LedgerEntryType(str, Enum):
    """The different ledger entry types"""

    ACCOUNT_ROOT = "AccountRoot"
    AMENDMENTS = "Amendments"
    AMM = "AMM"
    BRIDGE = "Bridge"
    CHECK = "Check"
    DEPOSIT_PREAUTH = "DepositPreauth"
    DID = "DID"
    DIRECTORY_NODE = "DirectoryNode"
    ESCROW = "Escrow"
    FEE_SETTINGS = "FeeSettings"
    LEDGER_HASHES = "LedgerHashes"
    NEGATIVE_UNL = "NegativeUNL"
    NFTOKEN_OFFER = "NFTokenOffer"
    NFTOKEN_PAGE = "NFTokenPage"
    OFFER = "Offer"
    PAY_CHANNEL = "PayChannel"
    RIPPLE_STATE = "RippleState"
    SIGNER_LIST = "SignerList"
    TICKET = "Ticket"
    XCHAIN_OWNED_CLAIM_ID = "XChainOwnedClaimID"
    XCHAIN_OWNED_CREATE_ACCOUNT_CLAIM_ID = "XChainOwnedCreateAccountClaimID"
