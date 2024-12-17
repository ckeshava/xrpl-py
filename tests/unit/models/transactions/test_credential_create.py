from unittest import TestCase

from xrpl.models.exceptions import XRPLModelException
from xrpl.models.transactions.credential_create import CredentialCreate
from xrpl.utils import str_to_hex

_ACCOUNT_ISSUER = "r9LqNeG6qHxjeUocjvVki2XR35weJ9mZgQ"
_ACCOUNT_SUBJECT = "rNdY9XDnQ4Dr1EgefwU3CBRuAjt3sAutGg"
_VALID_CREDENTIAL_TYPE = str_to_hex("Passport")
_VALID_URI = str_to_hex("www.my-id.com/username")


class TestCredentialCreate(TestCase):
    def test_valid(self):
        tx = CredentialCreate(
            account=_ACCOUNT_ISSUER,
            subject=_ACCOUNT_SUBJECT,
            credential_type=_VALID_CREDENTIAL_TYPE,
        )
        self.assertTrue(tx.is_valid())

    # invalid URI field inputs
    def test_uri_field_too_long(self):
        with self.assertRaises(XRPLModelException) as error:
            CredentialCreate(
                account=_ACCOUNT_ISSUER,
                subject=_ACCOUNT_SUBJECT,
                credential_type=_VALID_CREDENTIAL_TYPE,
                uri=str_to_hex("A" * 257),
            )
        self.assertEqual(
            error.exception.args[0],
            "{'uri': 'Length cannot exceed 128.'}",
        )

    def test_uri_field_empty(self):
        with self.assertRaises(XRPLModelException) as error:
            CredentialCreate(
                account=_ACCOUNT_ISSUER,
                subject=_ACCOUNT_SUBJECT,
                credential_type=_VALID_CREDENTIAL_TYPE,
                uri=str_to_hex(""),
            )
        self.assertEqual(
            error.exception.args[0],
            "{'uri': 'Length must be > 0.'}",
        )

    def test_uri_field_not_hex(self):
        with self.assertRaises(XRPLModelException) as error:
            CredentialCreate(
                account=_ACCOUNT_ISSUER,
                subject=_ACCOUNT_SUBJECT,
                credential_type=_VALID_CREDENTIAL_TYPE,
                uri="www.identity-repo.com/username",
            )
        self.assertEqual(
            error.exception.args[0],
            "{'uri': 'Must be encoded in hex.'}",
        )

    # invalid inputs to the credential_type field
    def test_cred_type_field_too_long(self):
        with self.assertRaises(XRPLModelException) as error:
            CredentialCreate(
                account=_ACCOUNT_ISSUER,
                subject=_ACCOUNT_SUBJECT,
                credential_type=str_to_hex("A" * 65),
                uri=_VALID_URI,
            )
        self.assertEqual(
            error.exception.args[0],
            "{'credential_type': 'Length must be less than 128.'}",
        )

    def test_cred_type_field_empty(self):
        with self.assertRaises(XRPLModelException) as error:
            CredentialCreate(
                account=_ACCOUNT_ISSUER,
                subject=_ACCOUNT_SUBJECT,
                credential_type="",
                uri=_VALID_URI,
            )
        self.assertEqual(
            error.exception.args[0],
            "{'credential_type': 'Length must be > 0.'}",
        )

    def test_cred_type_field_not_hex(self):
        with self.assertRaises(XRPLModelException) as error:
            CredentialCreate(
                account=_ACCOUNT_ISSUER,
                subject=_ACCOUNT_SUBJECT,
                credential_type="Passport",
                uri=_VALID_URI,
            )
        self.assertEqual(
            error.exception.args[0],
            "{'credential_type': 'credential_type field must be encoded in hex.'}",
        )

    def test_create_cred_type_object_all_empty_fields(self):
        with self.assertRaises(XRPLModelException):
            CredentialCreate(
                account=_ACCOUNT_ISSUER,
                subject=_ACCOUNT_SUBJECT,
                credential_type="",
                uri="",
            )
