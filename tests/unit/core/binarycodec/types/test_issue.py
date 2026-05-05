import unittest
from unittest import TestCase

from xrpl.core.binarycodec import XRPLBinaryCodecException
from xrpl.core.binarycodec.binary_wrappers.binary_parser import BinaryParser
from xrpl.core.binarycodec.types.issue import Issue


class TestIssue(TestCase):
    def test_from_value_xrp(self):
        issue_obj = Issue.from_value({"currency": "XRP"})
        self.assertEqual(issue_obj.to_json(), {"currency": "XRP"})

    def test_from_value_issued_currency(self):
        test_input = {"currency": "USD", "issuer": "rG1QQv2nh2gr7RCZ1P8YYcBUKCCN633jCn"}
        issue_obj = Issue.from_value(test_input)
        expected = {"currency": "USD", "issuer": "rG1QQv2nh2gr7RCZ1P8YYcBUKCCN633jCn"}
        self.assertEqual(issue_obj.to_json(), expected)

    def test_from_value_non_standard_currency(self):
        test_input = {
            "currency": "0123456789ABCDEF0123456789ABCDEF01234567",
            "issuer": "rG1QQv2nh2gr7RCZ1P8YYcBUKCCN633jCn",
        }
        issue_obj = Issue.from_value(test_input)
        expected = {
            "currency": "0123456789ABCDEF0123456789ABCDEF01234567",
            "issuer": "rG1QQv2nh2gr7RCZ1P8YYcBUKCCN633jCn",
        }
        self.assertEqual(issue_obj.to_json(), expected)

    def test_from_value_mpt(self):
        # Test Issue creation for an MPT currency.
        # Use a valid 48-character hex string (24 bytes) for mpt_issuance_id.
        test_input = {
            "mpt_issuance_id": "00001266F19FE2057AE426F72E923CAB3EC8E5BDB3341D9E",
        }
        issue_obj = Issue.from_value(test_input)
        expected = {
            "mpt_issuance_id": "00001266F19FE2057AE426F72E923CAB3EC8E5BDB3341D9E"
        }
        self.assertEqual(issue_obj.to_json(), expected)

    def test_short_mpt_issuance_id(self):
        # A valid mpt_issuance_id is 192 bits long (or 48 characters in hex).
        test_input = {
            "mpt_issuance_id": "A" * 47,
        }
        self.assertRaises(XRPLBinaryCodecException, Issue.from_value, test_input)

    def test_binary_representation_of_mpt_issuance_id(self):
        mpt_issuance_id_in_hex = "00001266F19FE2057AE426F72E923CAB3EC8E5BDB3341D9E"
        test_input = {
            "mpt_issuance_id": mpt_issuance_id_in_hex,
        }
        issue_obj = Issue.from_value(test_input)
        sequenceBE = (
            int.from_bytes(
                bytes.fromhex(mpt_issuance_id_in_hex[:8]),
                byteorder="little",
                signed=False,
            )
            .to_bytes(4, byteorder="big", signed=False)
            .hex()
            .upper()
        )

        self.assertEqual(
            issue_obj.to_hex(),
            # issuer_account's hex representation
            mpt_issuance_id_in_hex[8:48]
            # the below line is the hex representation of the
            # black-hole-account-id (ACCOUNT_ONE)
            + "0000000000000000000000000000000000000001"
            # sequence number's hex representation
            + sequenceBE,
        )
        self.assertEqual(issue_obj.to_json(), test_input)

    def test_from_parser_xrp(self):
        # Test round-trip: serialize an XRP Issue and then parse it back.
        test_input = {"currency": "XRP"}
        issue_obj = Issue.from_value(test_input)
        # For non-MPT cases, use the hex representation as input to the parser.
        parser = BinaryParser(issue_obj.to_hex())
        issue_from_parser = Issue.from_parser(parser)
        self.assertEqual(issue_from_parser.to_json(), {"currency": "XRP"})

    def test_from_parser_issued_currency(self):
        # Test round-trip: serialize an issued currency Issue and then parse it back.
        test_input = {"currency": "EUR", "issuer": "rLUEXYuLiQptky37CqLcm9USQpPiz5rkpD"}
        issue_obj = Issue.from_value(test_input)
        parser = BinaryParser(issue_obj.to_hex())
        issue_from_parser = Issue.from_parser(parser)
        expected = {"currency": "EUR", "issuer": "rLUEXYuLiQptky37CqLcm9USQpPiz5rkpD"}
        self.assertEqual(issue_from_parser.to_json(), expected)

    def test_from_parser_non_standard_currency(self):
        # Test round-trip conversion for non-standard currency codes.
        test_input = {
            "currency": "0123456789ABCDEF0123456789ABCDEF01234567",
            "issuer": "rLUEXYuLiQptky37CqLcm9USQpPiz5rkpD",
        }
        issue_obj = Issue.from_value(test_input)
        parser = BinaryParser(issue_obj.to_hex())
        issue_from_parser = Issue.from_parser(parser)
        expected = {
            "currency": "0123456789ABCDEF0123456789ABCDEF01234567",
            "issuer": "rLUEXYuLiQptky37CqLcm9USQpPiz5rkpD",
        }
        self.assertEqual(issue_from_parser.to_json(), expected)

    def test_from_parser_mpt(self):
        # Test round-trip: serialize an MPT Issue and then parse it back.
        test_input = {
            "mpt_issuance_id": "00001266F19FE2057AE426F72E923CAB3EC8E5BDB3341D9E",
        }
        issue_obj = Issue.from_value(test_input)
        # Use the hex representation
        parser = BinaryParser(issue_obj.to_hex())
        issue_from_parser = Issue.from_parser(parser)
        expected = {
            "mpt_issuance_id": "00001266F19FE2057AE426F72E923CAB3EC8E5BDB3341D9E"
        }
        self.assertEqual(issue_from_parser.to_json(), expected)

    def test_from_raw_hex_mpt(self):
        issuer_account_in_hex = "F19FE2057AE426F72E923CAB3EC8E5BDB3341D9E"
        sequence_little_endian_in_hex = "00001266"
        serialized_mpt_currency = (
            issuer_account_in_hex
            + "0000000000000000000000000000000000000001"
            + sequence_little_endian_in_hex
        )

        issue_from_parser = Issue.from_parser(BinaryParser(serialized_mpt_currency))
        sequence_in_hex = (
            int.from_bytes(
                bytes.fromhex(sequence_little_endian_in_hex),
                byteorder="little",
                signed=False,
            )
            .to_bytes(4, byteorder="big", signed=False)
            .hex()
            .upper()
        )

        expected = {
            "mpt_issuance_id": sequence_in_hex + issuer_account_in_hex,
        }
        self.assertEqual(issue_from_parser.to_json(), expected)

    def test_raises_invalid_value_type(self):
        # Test that providing an invalid input type raises an XRPLBinaryCodecException.
        invalid_value = 1
        self.assertRaises(XRPLBinaryCodecException, Issue.from_value, invalid_value)

    # The three tests below pin down a known inconsistency between Issue.from_value,
    # Issue.from_parser, and Issue.to_json for MPT issues — see xrpl.js #3332 and
    # rippled #7035. The 4-byte sequence portion of the wire layout
    # (issuer || NO_ACCOUNT || seq) is treated as little-endian by from_value /
    # to_json but stored verbatim by from_parser. A non-palindromic sequence
    # (0x00010203) is used so the byte reversal is visible byte-for-byte.

    _MPT_ISSUANCE_ID = "00010203E0739D43718DB5815CE070D4D514A261EC872C93"
    _ISSUER_HEX = "E0739D43718DB5815CE070D4D514A261EC872C93"
    _NO_ACCOUNT_HEX = "0000000000000000000000000000000000000001"
    # Wire blob with the sequence bytes in big-endian order (matching the byte
    # order of mpt_issuance_id itself).
    _WIRE_SEQ_BE = _ISSUER_HEX + _NO_ACCOUNT_HEX + "00010203"

    @unittest.expectedFailure
    def test_from_value_and_from_parser_be_wire_buffers_match(self):
        # Same logical MPT issue, two construction paths -> internal buffers
        # should be equal. They aren't: from_value stores seq LE, from_parser
        # stores it verbatim.
        from_json = Issue.from_value({"mpt_issuance_id": self._MPT_ISSUANCE_ID})
        from_wire = Issue.from_parser(BinaryParser(self._WIRE_SEQ_BE))
        self.assertEqual(from_json.to_hex().upper(), from_wire.to_hex().upper())

    @unittest.expectedFailure
    def test_from_parser_be_wire_round_trips_mpt_issuance_id(self):
        # Parsing a wire blob whose sequence bytes are big-endian (the byte
        # order of mpt_issuance_id) should yield JSON whose mpt_issuance_id
        # equals the input. Today, to_json reads the trailing 4 bytes as LE
        # and emits a byte-reversed sequence, e.g.
        #   expected: 00010203E0739D43...EC872C93
        #   actual:   03020100E0739D43...EC872C93
        from_wire = Issue.from_parser(BinaryParser(self._WIRE_SEQ_BE))
        self.assertEqual(
            from_wire.to_json(),
            {"mpt_issuance_id": self._MPT_ISSUANCE_ID},
        )

    @unittest.expectedFailure
    def test_to_json_consistent_across_construction_paths(self):
        # Constructing the same logical MPT issue from JSON and from a BE-seq
        # wire blob should yield the same JSON.
        from_json = Issue.from_value({"mpt_issuance_id": self._MPT_ISSUANCE_ID})
        from_wire = Issue.from_parser(BinaryParser(self._WIRE_SEQ_BE))
        self.assertEqual(from_json.to_json(), from_wire.to_json())
