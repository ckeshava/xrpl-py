from unittest import TestCase

from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.exceptions import XRPLModelException
from xrpl.models.transactions import Payment, PaymentFlag
from xrpl.wallet import Wallet

_ACCOUNT = "r9LqNeG6qHxjeUocjvVki2XR35weJ9mZgQ"
_FEE = "0.00001"
_SEQUENCE = 19048
_XRP_AMOUNT = "10000"
_ISSUED_CURRENCY_AMOUNT = IssuedCurrencyAmount(
    currency="BTC", value="1.002", issuer=_ACCOUNT
)
_DESTINATION = "rf1BiGeXwwQoi8Z2ueFYTEXSwuJYfV2Jpn"


class TestPayment(TestCase):
    def test_xrp_payment_with_paths(self):
        transaction_dict = {
            "account": _ACCOUNT,
            "fee": _FEE,
            "sequence": _SEQUENCE,
            "amount": _XRP_AMOUNT,
            "destination": _DESTINATION,
            "paths": ["random path stuff"],
        }
        with self.assertRaises(XRPLModelException):
            Payment(**transaction_dict)

    def test_xrp_payment_same_account_destination(self):
        transaction_dict = {
            "account": _ACCOUNT,
            "fee": _FEE,
            "sequence": _SEQUENCE,
            "amount": _XRP_AMOUNT,
            "destination": _ACCOUNT,
        }
        with self.assertRaises(XRPLModelException):
            Payment(**transaction_dict)

    def test_partial_payment_no_sendmax(self):
        transaction_dict = {
            "account": _ACCOUNT,
            "fee": _FEE,
            "sequence": _SEQUENCE,
            "amount": _ISSUED_CURRENCY_AMOUNT,
            "destination": _DESTINATION,
            "flags": PaymentFlag.TF_PARTIAL_PAYMENT,
        }
        with self.assertRaises(XRPLModelException):
            Payment(**transaction_dict)

    def test_deliver_min_no_partial_payment(self):
        transaction_dict = {
            "account": _ACCOUNT,
            "fee": _FEE,
            "sequence": _SEQUENCE,
            "amount": _ISSUED_CURRENCY_AMOUNT,
            "destination": _DESTINATION,
            "deliver_min": _ISSUED_CURRENCY_AMOUNT,
        }
        with self.assertRaises(XRPLModelException):
            Payment(**transaction_dict)

    def test_currency_conversion_no_sendmax(self):
        transaction_dict = {
            "account": _ACCOUNT,
            "fee": _FEE,
            "sequence": _SEQUENCE,
            "amount": _ISSUED_CURRENCY_AMOUNT,
            "destination": _ACCOUNT,
        }
        with self.assertRaises(XRPLModelException):
            Payment(**transaction_dict)

    def test_amount_send_max_xrp_no_partial_payment(self):
        transaction_dict = {
            "account": _ACCOUNT,
            "fee": _FEE,
            "sequence": _SEQUENCE,
            "amount": _XRP_AMOUNT,
            "send_max": _XRP_AMOUNT,
            "destination": _DESTINATION,
        }
        with self.assertRaises(XRPLModelException):
            Payment(**transaction_dict)

    def test_valid_xrp_payment(self):
        transaction_dict = {
            "account": _ACCOUNT,
            "fee": _FEE,
            "sequence": _SEQUENCE,
            "amount": _XRP_AMOUNT,
            "destination": _DESTINATION,
        }
        tx = Payment(**transaction_dict)
        self.assertTrue(tx.is_valid())

    def test_valid_issued_currency_payment(self):
        transaction_dict = {
            "account": _ACCOUNT,
            "fee": _FEE,
            "sequence": _SEQUENCE,
            "amount": _ISSUED_CURRENCY_AMOUNT,
            "send_max": _XRP_AMOUNT,
            "destination": _DESTINATION,
        }
        tx = Payment(**transaction_dict)
        self.assertTrue(tx.is_valid())

    def test_valid_partial_xrp_payment(self):
        transaction_dict = {
            "account": _ACCOUNT,
            "fee": _FEE,
            "sequence": _SEQUENCE,
            "amount": _XRP_AMOUNT,
            "send_max": _XRP_AMOUNT,
            "destination": _DESTINATION,
            "flags": PaymentFlag.TF_PARTIAL_PAYMENT,
        }
        tx = Payment(**transaction_dict)
        self.assertTrue(tx.is_valid())

    def test_destination_wallet(self):
        transaction_dict = {
            "account": _ACCOUNT,
            "fee": _FEE,
            "sequence": _SEQUENCE,
            "amount": _XRP_AMOUNT,
            "send_max": _XRP_AMOUNT,
            "destination": Wallet.create(),
        }
        with self.assertRaises(XRPLModelException):
            Payment(**transaction_dict)

    def test_credentials_array_empty(self):
        with self.assertRaises(XRPLModelException) as err:
            Payment(
                account=_ACCOUNT,
                amount=_XRP_AMOUNT,
                destination=_DESTINATION,
                credential_ids=[],
            )
        self.assertEqual(
            err.exception.args[0],
            "{'credential_ids': 'CredentialIDs list cannot be empty.'}",
        )

    def test_credentials_array_too_long(self):
        with self.assertRaises(XRPLModelException) as err:
            Payment(
                account=_ACCOUNT,
                amount=_XRP_AMOUNT,
                destination=_DESTINATION,
                credential_ids=["credential_index_" + str(i) for i in range(9)],
            )

        self.assertEqual(
            err.exception.args[0],
            "{'credential_ids': 'CredentialIDs list cannot have more than 8 "
            + "elements.'}",
        )
