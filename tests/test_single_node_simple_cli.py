import time
import json
import os

from hdacpy.transaction import Transaction as Tx
from hdacpy.wallet import mnemonic_to_privkey, mnemonic_to_address

import pytest

from .lib import cmd
from .lib.errors import DeadDaemonException, DaemonNotProducingBlock

class TestSingleNode():
    proc_ee = None
    proc_friday = None
    proc_rest = None

    chain_id = "testchain"
    moniker = "testnode"

    system_contract = "0000000000000000000000000000000000000000000000000000000000000000"
    anonymous_contract_address_hash = "fridaycontracthash1dl45lfet0wrsduxfeegwmskmmr8yhlpk6lk4qdpyhpjsffkymstq6ajv0a"
    anonymous_contract_address_uref = "fridaycontracturef1v4xev2kdy8hkzvwcadk4a3872lzcyyz8t44du5z2jhz636qduz3sf9mf96"

    wallet_elsa = "elsa"
    wallet_anna = "anna"
    wallet_olaf = "olaf"
    wallet_hans = "hans"
    wallet_password = "!friday1234@"

    nickname_elsa = "princesselsa"
    nickname_anna = "princessanna"

    info_elsa = None
    info_anna = None
    info_olaf = None
    info_hans = None

    basic_coin = "1000000000000000000000000000"
    basic_stake = "1000000000000000000"

    multiplier = 10 ** 18

    basic_coin_amount = int(int(basic_coin) / multiplier)

    basic_bond = "1"
    bonding_fee = "0.1"
    bonding_gas = 50000000

    delegate_amount = "1"
    delegate_amount_bigsun = "1000000000000000000"
    delegate_fee = "0.1"
    delegate_gas = 50000000

    vote_amount = "0.1"
    vote_amount_bigsun = "100000000000000000"
    vote_fee = "0.1"
    vote_gas = 50000000

    transfer_amount = "1"
    transfer_fee = "0.1"
    transfer_gas = 30000000

    short_gas = 10000000
    small_fee = "0.00001"

    tx_block_time = 6


    def daemon_healthcheck(self):
        is_ee_alive = cmd.daemon_check(self.proc_ee)
        is_friday_alive = cmd.daemon_check(self.proc_friday)
        is_rest_alive = cmd.daemon_check(self.proc_rest)
        for idx in range(5):
            try:
                res = cmd.get_block(1)
                if "error" not in res:
                    break

                print(res)
                print("Trial {}...".format(idx))

            except:
                print("Trial {}...".format(idx))
                print("Fail to get block. Sleep a little bit..")
                time.sleep(5)

        else:
            raise DaemonNotProducingBlock

        if not (is_ee_alive and is_friday_alive and is_rest_alive and "error" not in res):
            if not is_ee_alive:
                print("EE dead")

            if not is_friday_alive:
                print("Friday dead")

            if not is_rest_alive:
                print("REST server dead")

            raise DeadDaemonException


    def daemon_downcheck(self):
        is_ee_alive = cmd.daemon_check(self.proc_ee)
        is_friday_alive = cmd.daemon_check(self.proc_friday)
        is_rest_alive = cmd.daemon_check(self.proc_rest)

        if is_rest_alive:
            for _ in range(10):
                print("REST alive")
                self.proc_rest.kill()
                time.sleep(10)
                is_rest_alive = cmd.daemon_check(self.proc_rest)
                if not is_rest_alive:
                    break

            else:
                raise DeadDaemonException


        if is_friday_alive:
            for _ in range(10):
                print("Friday alive")
                self.proc_friday.kill()
                time.sleep(10)
                is_friday_alive = cmd.daemon_check(self.proc_friday)
                if not is_friday_alive:
                    break

            else:
                raise DeadDaemonException


        if is_ee_alive:
            for _ in range(10):
                print("EE alive")
                self.proc_ee.kill()
                time.sleep(10)
                is_ee_alive = cmd.daemon_check(self.proc_ee)
                if not is_ee_alive:
                    break

            else:
                raise DeadDaemonException


    def setup_class(self):
        """
        Make genesis.json and keys
        """
        print("*********************Test class preparation*********************")

        print("Cleanup double check")
        cmd.whole_cleanup()

        print("Init chain")
        cmd.init_chain(self.moniker, self.chain_id)
        print("Copy manifest file")
        cmd.copy_manifest()

        print("Create wallet")
        self.info_elsa = cmd.create_wallet(self.wallet_elsa, self.wallet_password)
        self.info_anna = cmd.create_wallet(self.wallet_anna, self.wallet_password)
        self.info_olaf = cmd.create_wallet(self.wallet_olaf, self.wallet_password)
        self.info_hans = cmd.create_wallet(self.wallet_hans, self.wallet_password)

        print("Collect info and make transaction sender")
        self.tx_elsa = Tx(
            chain_id=self.chain_id,
            host="http://localhost:1317",
            privkey=mnemonic_to_privkey(self.info_elsa["mnemonic"])
        )

        self.tx_anna = Tx(
            chain_id=self.chain_id,
            host="http://localhost:1317",
            privkey=mnemonic_to_privkey(self.info_anna["mnemonic"])
        )

        print("Apply general clif config")
        cmd.clif_configs(self.chain_id)

        print("Add genesis account in cosmos way")
        cmd.add_genesis_account(self.info_elsa['address'], self.basic_coin, self.basic_stake)
        cmd.add_genesis_account(self.info_anna['address'], self.basic_coin, self.basic_stake)
        cmd.add_genesis_account(self.info_olaf['address'], self.basic_coin, self.basic_stake)
        cmd.add_genesis_account(self.info_hans['address'], self.basic_coin, self.basic_stake)

        print("Add genesis account in EE way")
        cmd.add_el_genesis_account(self.wallet_elsa, self.basic_coin, self.basic_stake)
        cmd.add_el_genesis_account(self.wallet_anna, self.basic_coin, self.basic_stake)
        cmd.add_el_genesis_account(self.wallet_olaf, self.basic_coin, self.basic_stake)
        cmd.add_el_genesis_account(self.wallet_hans, self.basic_coin, self.basic_stake)

        print("Load chainspec")
        cmd.load_chainspec()

        print("Gentx")
        cmd.gentx(self.wallet_elsa, self.wallet_password)
        print("Collect gentxs")
        cmd.collect_gentxs()
        print("Validate genesis")
        cmd.validate_genesis()

        print("*********************Setup class done*********************")


    def teardown_class(self):
        """
        Delete all data and configs
        """
        print("Test finished and teardowning")
        cmd.delete_wallet(self.wallet_anna, self.wallet_password)
        cmd.delete_wallet(self.wallet_elsa, self.wallet_password)
        cmd.whole_cleanup()


    def setup_method(self):
        print("Waiting for running CasperLabs EE..")
        self.proc_ee = cmd.run_casperlabsEE()
        time.sleep(3)
        
        print("Waiting for running friday node..")
        self.proc_friday = cmd.run_node()
        # Waiting for nodef process is up and ready for receiving tx...
        time.sleep(10)

        print("Running rest server..")
        self.proc_rest = cmd.run_rest()

        self.daemon_healthcheck()
        print("Runup done. start testing")


    def teardown_method(self):
        print("Terminating daemons..")
        self.proc_rest.terminate()
        self.proc_friday.terminate()
        self.proc_ee.terminate()
        self.daemon_downcheck()

        print("Reset blocks")
        cmd.unsafe_reset_all()


    def test00_rest_get_balance(self):
        print("======================Start test00_rest_get_balance======================")
        
        res = self.tx_elsa.get_balance(self.info_elsa['address'])
        print("Output: ", res)
        assert(float(res["stringValue"]) / self.multiplier == self.basic_coin_amount) 

        res = self.tx_anna.get_balance(self.info_anna['address'])
        print("Output: ", res)
        assert(float(res["stringValue"]) / self.multiplier == self.basic_coin_amount)

        print("======================Done test00_rest_get_balance======================")


    def test01_rest_transfer_to(self):
        print("======================Start test01_rest_transfer_to======================")

        print("Transfer token from elsa to anna")
        res = self.tx_elsa.transfer(self.info_anna['address'], self.transfer_amount,
                        self.transfer_gas, self.transfer_fee)
        print(res)
        
        print("Tx sent. Waiting for validation")
        time.sleep(self.tx_block_time * 3 + 1)

        print("Check whether tx is ok or not")
        is_ok = cmd.is_tx_ok(res["txhash"])
        assert(is_ok == True)

        print("Balance checking after transfer..")
        res = self.tx_anna.get_balance(self.info_anna['address'])
        assert(int(res["stringValue"]) / self.multiplier == self.basic_coin_amount + int(self.transfer_amount))

        res = self.tx_elsa.get_balance(self.info_elsa['address'])
        assert(int(res["stringValue"]) / self.multiplier <  self.basic_coin_amount - int(self.transfer_amount))

        print("======================Done test01_rest_transfer_to======================")


    def test02_rest_bond_and_unbond(self):
        print("======================Start test02_rest_bond_and_unbond======================")

        print("Bonding token")
        bond_tx_res = self.tx_anna.bond(self.basic_coin_amount / 3, self.bonding_gas, self.bonding_fee)
        print("Tx sent. Waiting for validation")

        time.sleep(self.tx_block_time * 3 + 1)

        print("Check whether tx is ok or not")
        bond_tx_hash = bond_tx_res['txhash']
        bond_tx_check_res = self.tx_anna.get_tx(bond_tx_hash)
        is_ok = cmd.tx_validation(bond_tx_check_res)
        assert(is_ok == True)

        print("Balance checking after bonding")
        res_before = self.tx_anna.get_balance(self.info_anna['address'])
        print("Output: ", res_before)
        assert(2 * 0.99 * self.basic_coin_amount / 3 < float(res_before["stringValue"]) / self.multiplier < 2 * self.basic_coin_amount / 3)

        print("Try to send more money than bonding. Invalid tx expected")
        tx_hash_after_bond = self.tx_anna.transfer(
                                self.info_elsa['address'], self.basic_coin_amount * 2 / 3,
                                self.transfer_gas, self.transfer_fee
                             )
        
        print("Tx sent. Waiting for validation")
        time.sleep(self.tx_block_time * 3 + 1)
        
        print("Check whether tx is ok or not")
        tx_hash_after_bond_hash = tx_hash_after_bond['txhash']
        tx_hash_after_bond_res = self.tx_anna.get_tx(tx_hash_after_bond_hash)
        is_ok = cmd.tx_validation(tx_hash_after_bond_res)
        assert(is_ok == False)

        print("Balance checking after bonding")
        res_after = self.tx_anna.get_balance(self.info_anna['address'])
        # Reason: Just enough value to ensure that tx become invalid
        print("Output: ", res_after)
        assert(2 * 0.99 * self.basic_coin_amount / 3 < float(res_after["stringValue"]) / self.multiplier < 2 * self.basic_coin_amount / 3)


        print("Unbond and try to transfer")
        print("Unbond first")
        tx_unbond_res = self.tx_anna.unbond(self.basic_coin_amount / 30, self.bonding_gas, self.bonding_fee)
        print("Tx sent. Waiting for validation")

        time.sleep(self.tx_block_time * 3 + 1)

        print("Check whether tx is ok or not")
        print(tx_unbond_res)
        is_ok = cmd.tx_validation(tx_unbond_res)
        assert(is_ok == True)

        print("Balance checking after unbonding")
        res_after = self.tx_anna.get_balance(self.info_anna['address'])
        # Reason: Just enough value to ensure that tx become invalid
        print("Output: ", res_after)

        print("Try to transfer. Will be confirmed in this time")
        tx_hash_after_unbond = self.tx_anna.transfer(
                                self.info_elsa['address'], self.basic_coin_amount * 2 / 3,
                                self.transfer_gas, self.transfer_fee
                               )
        
        print("Tx sent. Waiting for validation")
        time.sleep(self.tx_block_time * 3 + 1)

        print("Check whether tx is ok or not")
        tx_hash_after_unbond_res = self.tx_anna.get_tx(tx_hash_after_unbond['txhash'])
        is_ok = cmd.tx_validation(tx_hash_after_unbond_res)
        assert(is_ok == True)

        print("Balance checking after transfer")
        res_after_after = self.tx_anna.get_balance(self.info_anna['address'])
        print("Output: ", res_after_after)
        assert(float(res_after_after["stringValue"]) / self.multiplier < self.basic_coin_amount / 30)

        print("======================Done test02_rest_bond_and_unbond======================")


    def test03_rest_custom_contract_execution(self):
        print("======================Start test03_rest_custom_contract_execution======================")
        print("Run store system contract")

        print("Try to run bond function by wasm path")
        wasm_path = os.path.join(os.environ['HOME'], ".nodef", "contracts", "bonding.wasm")
        param = json.dumps([
            {
                "name":"amount",
                "value":{
                    "clType":{
                        "simpleType":"U512"
                    },
                    "value":{
                        "u512":{
                        "value":"10000000000000000"
                        }
                    }
                }
            }
        ])
        wasm_bin = None
        with open(wasm_path, 'rb') as f:
            f_bin = f.read()

            import base64
            wasm_bin = base64.b64encode(f_bin).decode('utf-8')

        tx_store_contract = self.tx_anna.execute_contract("wasm", "", wasm_bin, param, self.bonding_gas, self.bonding_fee)
        print("Tx sent. Waiting for validation")
        time.sleep(self.tx_block_time * 3 + 1)
        tx_check_store_contract_res = self.tx_anna.get_tx(tx_store_contract['txhash'])
        print("Check Tx OK or not")

        is_ok = cmd.tx_validation(tx_check_store_contract_res)
        assert(is_ok == True)

        print("Check contract query")
        res = self.tx_anna.query_contract("address", "system", "")
        print(res)
        print("======================End test03_rest_custom_contract_execution======================")


    def test04_rest_simple_delegate_redelegate_and_undelegate(self):
        print("======================Start test04_rest_simple_delegate_redelegate_and_undelegate======================")

        print("Delegate token")
        delegate_tx_res = self.tx_anna.delegate(self.info_elsa['address'], self.delegate_amount, self.delegate_gas, self.delegate_fee)
        print("Tx sent. Waiting for delegate")

        time.sleep(self.tx_block_time * 3 + 1)

        print("Check whether tx is ok or not")
        delegate_check_tx_res = self.tx_anna.get_tx(delegate_tx_res['txhash'])
        is_ok = cmd.tx_validation(delegate_check_tx_res)
        assert(is_ok == True)

        delegator_res = self.tx_anna.get_delegator(self.info_elsa['address'], self.info_anna['address'])
        print("Output: ", delegator_res)
        assert(delegator_res[0]["amount"] == self.delegate_amount_bigsun) 

        print("Redelegate token")
        redelegate_tx_res = self.tx_anna.redelegate(self.info_elsa['address'], self.info_olaf['address'], self.delegate_amount, self.delegate_gas, self.delegate_fee)
        print("Tx sent. Waiting for redelegate")

        time.sleep(self.tx_block_time * 3 + 1)

        print("Check whether tx is ok or not")
        redelegate_check_tx_res = self.tx_anna.get_tx(redelegate_tx_res['txhash'])
        is_ok = cmd.tx_validation(redelegate_check_tx_res)
        assert(is_ok == True)

        delegator_res = self.tx_anna.get_delegator(self.info_olaf['address'], self.info_anna['address'])
        print("Output: ", delegator_res)
        assert(delegator_res[0]["amount"] == self.delegate_amount_bigsun) 

        print("Undelegate token")
        undelegate_tx_res = self.tx_anna.undelegate(self.info_olaf['address'], self.delegate_amount, self.delegate_gas, self.delegate_fee)
        print("Tx sent. Waiting for undelegate")

        time.sleep(self.tx_block_time * 3 + 1)

        print("Check whether tx is ok or not")
        undelegate_check_tx_res = self.tx_anna.get_tx(undelegate_tx_res['txhash'])
        is_ok = cmd.tx_validation(undelegate_check_tx_res)
        assert(is_ok == True)

        print("======================Done test04_rest_simple_delegate_redelegate_and_undelegate======================")


    def test05_rest_simple_vote_and_unvote(self):
        print("======================Start test05_rest_simple_vote_and_unvote======================")

        print("Vote token: uref")
        vote_uref_tx_res = self.tx_anna.vote(self.anonymous_contract_address_uref, self.vote_amount, self.vote_gas, self.vote_fee)
        print("Tx sent. Waiting for vote")

        time.sleep(self.tx_block_time * 3 + 1)

        print("Check whether tx is ok or not")
        vote_uref_check_tx_res = self.tx_anna.get_tx(vote_uref_tx_res['txhash'])
        is_ok = cmd.tx_validation(vote_uref_check_tx_res)
        assert(is_ok == True)

        voter_res = self.tx_anna.get_voter(self.info_anna['address'], self.anonymous_contract_address_uref)
        print("Output: ", voter_res)
        assert(voter_res[0]["amount"] == self.vote_amount_bigsun)

        print("Vote token: hash")
        vote_hash_tx_res = self.tx_anna.vote(self.anonymous_contract_address_hash, self.vote_amount, self.vote_gas, self.vote_fee)
        print("Tx sent. Waiting for vote")

        time.sleep(self.tx_block_time * 3 + 1)

        print("Check whether tx is ok or not")
        vote_hash_check_tx_res = self.tx_anna.get_tx(vote_hash_tx_res['txhash'])
        is_ok = cmd.tx_validation(vote_hash_check_tx_res)
        assert(is_ok == True)

        voter_res = self.tx_anna.get_voter(self.info_anna['address'], self.anonymous_contract_address_hash)
        print("Output: ", voter_res)
        assert(voter_res[0]["amount"] == self.vote_amount_bigsun) 

        print("Unvote token")
        unvote_hash_tx_res = self.tx_anna.unvote(self.anonymous_contract_address_hash, self.vote_amount, self.vote_gas, self.vote_fee)
        print("Tx sent. Waiting for unvote")

        time.sleep(self.tx_block_time * 3 + 1)

        print("Check whether tx is ok or not")
        unvote_hash_check_tx_res = self.tx_anna.get_tx(unvote_hash_tx_res['txhash'])
        is_ok = cmd.tx_validation(unvote_hash_check_tx_res)
        assert(is_ok == True)

        print("Check malfunction: wrong address")
        try:
            _ = self.tx_anna.vote(self.system_contract, self.vote_amount, self.vote_gas, self.vote_fee)
            raise Exception("Executed. Test fails")

        except:
            print("Expected error occurred. Success")

        print("======================Done test05_rest_simple_vote_and_unvote======================")


    def test06_rest_simple_claim_reward_and_commission(self):
        print("======================Start test06_rest_simple_claim_reward_and_commission======================")

        time.sleep(self.tx_block_time * 3 + 1)

        res = self.tx_anna.get_balance(self.info_anna['address'])
        init_balance = float(res["stringValue"])
        assert(init_balance / self.multiplier == self.basic_coin_amount) 

        commission_query_res = self.tx_anna.get_commission(self.info_anna['address'])
        print("Output: ", commission_query_res)
        commission_value = float(commission_query_res["stringValue"])
        assert(commission_value / self.multiplier > 0) 

        reward_query_res = self.tx_anna.get_reward(self.info_anna['address'])
        print("Output: ", reward_query_res)
        reward_value = float(reward_query_res["stringValue"])
        assert(reward_value / self.multiplier > 0) 

        print("Claim reward token")
        claim_reward_tx_hash = self.tx_anna.claim(True, self.vote_gas, self.vote_fee)
        
        print("Tx sent. Waiting for claim reward")
        time.sleep(self.tx_block_time * 3 + 1)

        claim_reward_check_tx_res = self.tx_anna.get_tx(claim_reward_tx_hash['txhash'])
        is_ok = cmd.tx_validation(claim_reward_check_tx_res)
        assert(is_ok == True)

        res = self.tx_anna.get_balance(self.info_anna['address'])
        add_reward_balance = float(res["stringValue"])
        print("Output: ", res)
        assert(float(init_balance) / self.multiplier < add_reward_balance)

        print("Claim commission token")
        claim_commission_tx_hash = self.tx_anna.claim(False, self.vote_gas, self.vote_fee)
        
        print("Tx sent. Waiting for claim commission")
        time.sleep(self.tx_block_time * 3 + 1)
        
        claim_commission_check_tx_res = self.tx_anna.get_tx(claim_commission_tx_hash['txhash'])
        is_ok = cmd.tx_validation(claim_commission_check_tx_res)
        assert(is_ok == True)

        res = self.tx_anna.get_balance(self.info_anna['address'])
        print("Output: ", res)
        add_reward_and_commission_balance = float(res["stringValue"])
        assert(add_reward_balance < add_reward_and_commission_balance)

        print("======================Done test06_rest_simple_claim_reward_and_commission======================")


    def test09_rest_transfer_should_fail_due_to_fee_shortage(self):
        print("======================Start test09_rest_transfer_should_fail_due_to_fee_shortage======================")

        print("Try to transfer token from elsa to anna. This tx should fail due to small fee in execution engine")
        tx_res = self.tx_elsa.transfer(self.info_anna['address'], self.transfer_amount,
                        self.short_gas, self.small_fee)
        
        print("Tx sent. Waiting for validation")
        time.sleep(self.tx_block_time * 3 + 1)

        print("Check whether tx is ok or not")
        check_tx_res = self.tx_anna.get_tx(tx_res['txhash'])
        is_ok = cmd.tx_validation(check_tx_res)
        assert(is_ok == False)

        print("======================Done test09_rest_transfer_should_fail_due_to_fee_shortage======================")
