import time

from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.it_utils import (
    sign_and_reliable_submission_async,
    test_async_and_sync,
)
from tests.integration.reusable_values import WALLET
from xrpl.core.addresscodec.main import MAX_32_BIT_UNSIGNED_INT
from xrpl.models import AccountObjects, AccountObjectType, OracleSet
from xrpl.models.response import ResponseStatus
from xrpl.models.transactions.oracle_set import PriceData
from xrpl.utils import str_to_hex

_PROVIDER = str_to_hex("provider")
_ASSET_CLASS = str_to_hex("currency")


class TestSetOracle(IntegrationTestCase):
    @test_async_and_sync(globals())
    async def test_all_fields(self, client):
        tx = OracleSet(
            account=WALLET.address,
            # if oracle_document_id is not modified, the (sync, async) +
            # (json, websocket) combination of integration tests will update the same
            # oracle object using identical "LastUpdateTime". Updates to an oracle must
            # be more recent than its previous LastUpdateTime
            # a unique value is obtained for each combination of test run within the
            # implementation of the test_async_and_sync decorator.
            oracle_document_id=self.value,
            provider=_PROVIDER,
            asset_class=_ASSET_CLASS,
            last_update_time=int(time.time()),
            price_data_series=[
                PriceData(
                    base_asset="XRP", quote_asset="USD", asset_price=740, scale=1
                ),
                PriceData(
                    base_asset="BTC", quote_asset="EUR", asset_price=100, scale=2
                ),
            ],
        )
        response = await sign_and_reliable_submission_async(tx, WALLET, client)
        self.assertEqual(response.status, ResponseStatus.SUCCESS)
        self.assertEqual(response.result["engine_result"], "tesSUCCESS")

        # confirm that the PriceOracle was actually created
        account_objects_response = await client.request(
            AccountObjects(account=WALLET.address, type=AccountObjectType.ORACLE)
        )

        # subsequent integration tests (sync/async + json/websocket) add one
        # oracle object to the account
        self.assertTrue(len(account_objects_response.result["account_objects"]) > 0)

    @test_async_and_sync(globals())
    async def test_large_asset_price(self, client):
        tx = OracleSet(
            account=WALLET.address,
            # if oracle_document_id is not modified, the (sync, async) +
            # (json, websocket) combination of integration tests will update the same
            # oracle object using identical "LastUpdateTime". Updates to an oracle must
            # be more recent than its previous LastUpdateTime
            # a unique value is obtained for each combination of test run within the
            # implementation of the test_async_and_sync decorator.
            oracle_document_id=self.value,
            provider=_PROVIDER,
            asset_class=_ASSET_CLASS,
            last_update_time=int(time.time()),
            price_data_series=[
                PriceData(
                    base_asset="XRP",
                    quote_asset="USD",
                    asset_price=MAX_32_BIT_UNSIGNED_INT,
                    scale=1,
                ),
                PriceData(
                    base_asset="BTC",
                    quote_asset="EUR",
                    asset_price=MAX_32_BIT_UNSIGNED_INT + 10,
                    scale=2,
                ),
            ],
        )
        response = await sign_and_reliable_submission_async(tx, WALLET, client)
        self.assertEqual(response.status, ResponseStatus.SUCCESS)
        self.assertEqual(response.result["engine_result"], "tesSUCCESS")
        self.assertEqual(
            response.result["tx_json"]["PriceDataSeries"][0]["PriceData"]["AssetPrice"],
            "ffffffff",  # hexadecimal representation of MAX_32_BIT_UNSIGNED_INT
        )

        self.assertEqual(
            response.result["tx_json"]["PriceDataSeries"][1]["PriceData"]["AssetPrice"],
            # hexadecimal representation of MAX_32_BIT_UNSIGNED_INT + 10 == 4294967305
            "100000009",
        )

        # confirm that the PriceOracle was actually created
        account_objects_response = await client.request(
            AccountObjects(account=WALLET.address, type=AccountObjectType.ORACLE)
        )

        # subsequent integration tests (sync/async + json/websocket) add one
        # oracle object to the account
        self.assertTrue(len(account_objects_response.result["account_objects"]) > 0)
