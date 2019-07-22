import os
import pytest
import eth_tester
from pytest import raises

from web3 import Web3
from web3.contract import ConciseContract
from web3.providers.eth_tester import (EthereumTesterProvider)
from eth_tester import (EthereumTester)
from eth_tester.exceptions import TransactionFailed
from vyper import compiler

setattr(eth_tester.main, 'GENESIS_GAS_LIMIT', 10**9)
setattr(eth_tester.main, 'GENESIS_DIFFICULTY', 1)


@pytest.fixture
def tester():
    return EthereumTester()


@pytest.fixture
def w3(tester):
    w3 = Web3(EthereumTesterProvider(tester))
    w3.eth.setGasPriceStrategy(lambda web3, params: 0)
    w3.eth.defaultAccount = w3.eth.accounts[0]
    return w3


def _get_contract(w3, path, *args):
    wd = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(wd, os.pardir, path)) as f:
        source = f.read()
    out = compiler.compile_code(
        source, ['abi', 'bytecode'], interface_codes=None)
    deploy = w3.eth.contract(abi=out['abi'], bytecode=out['bytecode'])
    tx_hash = deploy.constructor(*args).transact()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    return ConciseContract(
        w3.eth.contract(address=tx_receipt.contractAddress, abi=out['abi']))


@pytest.fixture
def get_contract(w3):
    def get_contract(source_code, *args, **kwargs):
        return _get_contract(w3, source_code, *args, **kwargs)

    return get_contract


@pytest.fixture
def SOCKSERC20(w3, get_contract):
    return get_contract('contracts/test_contracts/socksclassic.vy')


@pytest.fixture
def SOCKSERC721(w3, get_contract):
    return get_contract('contracts/socksclassic.vy')


@pytest.fixture
def REDEEM(w3, get_contract, SOCKSERC20, SOCKSERC721):
    return get_contract('contracts/redeemcontract.vy', SOCKSERC20.address,
                        SOCKSERC721.address)


@pytest.fixture
def assert_fail():
    def assert_fail(func):
        with raises(Exception):
            func()

    return assert_fail


@pytest.fixture
def assert_tx_failed(tester):
    def assert_tx_failed(function_to_test,
                         exception=TransactionFailed,
                         exc_text=None):
        snapshot_id = tester.take_snapshot()
        with pytest.raises(exception) as excinfo:
            function_to_test()
        tester.revert_to_snapshot(snapshot_id)
        if exc_text:
            assert exc_text in str(excinfo.value)

    return assert_tx_failed
