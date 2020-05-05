import json
import pytest
from unittest.mock import Mock

from hdacpy.transaction import Transaction


def test_sign():
    private_key = "2afc5a66b30e7521d553ec8e6f7244f906df97477248c30c103d7b3f2c671fef"
    unordered_sign_message = {
        "chain_id": "friday-devtest",
        "account_number": "1",
        "fee": {"gas": "21906", "amount": [{"amount": "0", "denom": ""}]},
        "memo": "",
        "sequence": "0",
        "msgs": [
            {
                "type": "cosmos-sdk/Send",
                "value": {
                    "inputs": [
                        {
                            "address": "friday1qperwt9wrnkg5k9e5gzfgjppzpqhyav5j24d66",
                            "coins": [{"amount": "1", "denom": "STAKE"}],
                        }
                    ],
                    "outputs": [
                        {
                            "address": "friday1yeckxz7tapz34kjwnjxvmxzurerquhtrmxmuxt",
                            "coins": [{"amount": "1", "denom": "STAKE"}],
                        }
                    ],
                },
            }
        ],
    }

    tx = Transaction(
        host="http://localhost:1317",
        privkey=private_key,
        chain_id="friday-devnet",
    )
    tx._get_sign_message = Mock(return_value=unordered_sign_message)  # type: ignore

    expected_signature = (
        "5YvLtcxp3BzxCTGM6TlKZ//nNBakmWyUrvydJgOCeQAc5DnFEnm5/Q48zEtEHy0dS3iNB7KH/ykqcYnWGHWbNQ=="
    )

    actual_signature = tx._sign()
    assert actual_signature == expected_signature
