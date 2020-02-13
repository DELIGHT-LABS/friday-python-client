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


@pytest.mark.skip(reason="only works if RESTful server runs in local")
def test_transfer():
    _tx_total_cost = 200000000
    fee = 100000000
    amount = _tx_total_cost - fee

    tx = Transaction(
        host="http://localhost:1317",
        privkey="26d167d549a4b2b66f766b0d3f2bdbe1cd92708818c338ff453abde316a2bd59",
        chain_id="friday-devnet",
    )
    tx.transfer(
        token_contract_address="friday15evpva2u57vv6l5czehyk69s0wnq9hrkqulwfz",
        recipient_address="friday1z47ev5u5ujmc7kwv49tut7raesg55tjyk2wvhd",
        amount=amount, gas_price=20000000, fee=fee
    )

    res = tx.send_tx()
    resp = res.json()
    resp['tx']['msg'][0]['value'].pop('session_code')
    resp['tx']['msg'][0]['value'].pop('payment_code')

    assert res.status_code == 200


@pytest.mark.skip(reason="only works if RESTful server runs in local")
def test_bond():
    _tx_total_cost = 388000
    fee = 1000
    amount = _tx_total_cost - fee

    tx = Transaction(
        host="http://localhost:1317",
        privkey="26d167d549a4b2b66f766b0d3f2bdbe1cd92708818c338ff453abde316a2bd59",
        chain_id="friday-devnet",
    )
    tx.bond(
        token_contract_address="friday1lgharzgds89lpshr7q8kcmd2esnxkfpwmfgk32",
        amount=amount, gas_price=2000000, fee=10000
    )

    res_without_bin = tx._get_pushable_tx()
    res_without_bin['tx']['msg'][0]['value'].pop('session_code')
    res_without_bin['tx']['msg'][0]['value'].pop('payment_code')

    res = tx.send_tx()
    assert res.status_code == 200


@pytest.mark.skip(reason="only works if RESTful server runs in local")
def test_unbond():
    _tx_total_cost = 388000
    fee = 1000
    amount = _tx_total_cost - fee

    tx = Transaction(
        host="http://localhost:1317",
        privkey="26d167d549a4b2b66f766b0d3f2bdbe1cd92708818c338ff453abde316a2bd59",
        chain_id="friday-devtest",
    )
    tx.unbond(
        token_contract_address="friday1lgharzgds89lpshr7q8kcmd2esnxkfpwmfgk32",
        amount=amount, gas_price=2000000, fee=10000
    )

    res_without_bin = tx._get_pushable_tx()
    res_without_bin['tx']['msg'][0]['value'].pop('session_code')
    res_without_bin['tx']['msg'][0]['value'].pop('payment_code')

    res = tx.send_tx()
    assert res.status_code == 200


@pytest.mark.skip(reason="only works if RESTful server runs in local")
def test_setnick():
    tx = Transaction(
        host="http://localhost:1317",
        privkey="26d167d549a4b2b66f766b0d3f2bdbe1cd92708818c338ff453abde316a2bd59",
        chain_id="friday-devtest",
    )
    tx.set_nick(name="bryan", gas_price=2000000)
    res = tx.send_tx()
    resp = res.json()
    assert res.status_code == 200 and resp['code'] == 0


@pytest.mark.skip(reason="only works if RESTful server runs in local")
def test_changekey():
    tx = Transaction(
        host="http://localhost:1317",
        privkey="26d167d549a4b2b66f766b0d3f2bdbe1cd92708818c338ff453abde316a2bd59",
        chain_id="testnet",
    )
    tx.changekey(
        name="bryan",
        newpubkey="0356fab26b795d07fee213444c553f544713911253ca744bd38d9e6e2d648bc8c4",
        gas_price=2000000)
    res = tx.send_tx()
    resp = res.json()
    assert res.status_code == 200 and resp['code'] == 0

@pytest.mark.skip(reason="only works if RESTful server runs in local")
def test_create_validator():
    _tx_total_cost = 388000
    fee = 1000
    amount = _tx_total_cost - fee

    tx = Transaction(
        host="http://localhost:1317",
        privkey="26d167d549a4b2b66f766b0d3f2bdbe1cd92708818c338ff453abde316a2bd59",
        chain_id="friday-devtest",
    )
    tx.create_validator(
        validator_address="friday1lgharzgds89lpshr7q8kcmd2esnxkfpwmfgk32",
        cons_pub_key="fridayvalconspub16jrl8jvqqyukck2p89czk4zfdp4hvjn9f96kswr08yh5g3p0w9xnvd2xw4q5vumpfpmhqezwxpvrz6r02f44v569xqe82wt6x4fx2vj5veynq66z2f9xw3jgfqmxkv2ffegr26j9g35xj633dg68venefpey5mj0xeu5jun2xq6x2c2nwagx75rgxef5guj9gaa85cm5wax9542tx4xng5qlp58f4",
        moniker="validator1",
        identity="",
        website="",
        details="",
        gas_price=2000000,
        memo="",
    )

    res = tx.send_tx()
    resp = res.json()

    assert res.status_code == 200


@pytest.mark.skip(reason="only works if RESTful server runs in local")
def test_edit_validator():
    _tx_total_cost = 388000
    fee = 1000
    amount = _tx_total_cost - fee

    tx = Transaction(
        host="http://localhost:1317",
        privkey="26d167d549a4b2b66f766b0d3f2bdbe1cd92708818c338ff453abde316a2bd59",
        chain_id="friday-devtest",
    )
    tx.edit_validator(
        validator_address="friday1lgharzgds89lpshr7q8kcmd2esnxkfpwmfgk32",
        moniker="validator2",
        identity="",
        website="hdac.io",
        details="",
        gas_price=2000000,
        memo="",
    )

    res = tx.send_tx()
    resp = res.json()

    assert res.status_code == 200
