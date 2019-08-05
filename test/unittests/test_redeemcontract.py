from test.constants import (
    DECIMALS, )


def test_init(w3, REDEEM, SOCKSERC20):
    a0, a1 = w3.eth.accounts[:2]
    assert REDEEM.token() == SOCKSERC20.address


def test_redeem(w3, REDEEM, SOCKSERC20, SOCKSERC721, assert_tx_failed):
    a0, a1 = w3.eth.accounts[:2]
    assert SOCKSERC721.totalSupply() == 0
    assert_tx_failed(lambda: REDEEM.redeem(0, transact={'from': a0}))
    assert_tx_failed(lambda: REDEEM.redeem(1, transact={'from': a0}))
    SOCKSERC20.approve(REDEEM.address, 1 * DECIMALS, transact={'from': a0})
    assert_tx_failed(lambda: REDEEM.redeem(1, transact={'from': a0}))
    assert SOCKSERC20.totalSupply() == 500 * DECIMALS
    SOCKSERC721.addMinter(REDEEM.address, transact={'from': a0})
    assert SOCKSERC721.minters(REDEEM.address)

    REDEEM.redeem(1, transact={'from': a0})
    assert SOCKSERC20.totalSupply() == (500 - 1) * DECIMALS
    assert SOCKSERC721.totalSupply() == 1

    assert_tx_failed(lambda: REDEEM.redeem(1, transact={'from': a0}))
    assert SOCKSERC20.totalSupply() == (500 - 1) * DECIMALS

    SOCKSERC20.approve(REDEEM.address, 1 * 10**18, transact={'from': a0})
    REDEEM.redeem(1, transact={'from': a0})
    assert SOCKSERC20.totalSupply() == (500 - 2) * DECIMALS
    assert REDEEM.tokensMinted() == 2


def test_redeem_several(w3, REDEEM, SOCKSERC20, SOCKSERC721, assert_tx_failed,
                        get_logs):
    a0, a1 = w3.eth.accounts[:2]
    SOCKSERC20.approve(REDEEM.address, 500 * DECIMALS, transact={'from': a0})
    SOCKSERC721.addMinter(REDEEM.address, transact={'from': a0})

    tx_hash = REDEEM.redeem(9, transact={'from': a0})
    redeem_logs = get_logs(tx_hash, REDEEM, 'Redemption')
    assert REDEEM.tokensMinted() == 9
    assert len(redeem_logs) == 9
    assert redeem_logs[len(redeem_logs) - 1].args._tokenId == 8

    assert SOCKSERC721.totalSupply() == 9


def test_change_erc20_address(w3, SOCKSERC20, SOCKSERC721, REDEEM,
                              assert_tx_failed):
    a0, a1 = w3.eth.accounts[:2]
    assert (REDEEM.token() == SOCKSERC20.address)
    assert_tx_failed(lambda: REDEEM.change_token_address(
        SOCKSERC721.address, transact={'from': a1}))
    REDEEM.change_token_address(SOCKSERC721.address, transact={'from': a0})
    assert (REDEEM.token() == SOCKSERC721.address)


def test_change_erc721_address(w3, SOCKSERC20, SOCKSERC721, REDEEM,
                               assert_tx_failed):
    a0, a1 = w3.eth.accounts[:2]
    assert (REDEEM.nft() == SOCKSERC721.address)
    assert_tx_failed(lambda: REDEEM.change_token_address(
        SOCKSERC20.address, transact={'from': a1}))
    REDEEM.change_token_address(SOCKSERC20.address, transact={'from': a0})
    assert (REDEEM.token() == SOCKSERC20.address)


def test_change_starting_index(w3, SOCKSERC20, SOCKSERC721, REDEEM,
                               assert_tx_failed, get_logs):
    a0, a1 = w3.eth.accounts[:2]
    SOCKSERC20.approve(REDEEM.address, 500 * DECIMALS, transact={'from': a0})
    SOCKSERC721.addMinter(REDEEM.address, transact={'from': a0})
    REDEEM.setStartingIndex(10, transact={'from': a0})

    tx_hash = REDEEM.redeem(1, transact={'from': a0})
    assert REDEEM.tokensMinted() == 1
    assert SOCKSERC721.totalSupply() == 1
    assert SOCKSERC721.ownerOf(10) == a0

    redeem_logs = get_logs(tx_hash, REDEEM, 'Redemption')
    assert len(redeem_logs) == 1
    assert redeem_logs[0].args._tokenId == 10
