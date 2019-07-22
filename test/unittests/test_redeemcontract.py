def test_init(w3, REDEEM, SOCKSERC20):
    a0, a1 = w3.eth.accounts[:2]
    assert REDEEM.token() == SOCKSERC20.address


def test_redeem(w3, REDEEM, SOCKSERC20, SOCKSERC721, assert_tx_failed):
    a0, a1 = w3.eth.accounts[:2]
    assert SOCKSERC721.totalSupply() == 0
    assert_tx_failed(lambda: REDEEM.redeem(0, transact={'from': a0}))
    assert_tx_failed(lambda: REDEEM.redeem(1, transact={'from': a0}))
    SOCKSERC20.approve(REDEEM.address, 1, transact={'from': a0})
    assert_tx_failed(lambda: REDEEM.redeem(1, transact={'from': a0}))
    assert SOCKSERC20.totalSupply() == 500 * 10**18
    SOCKSERC721.addMinter(REDEEM.address, transact={'from': a0})
    assert SOCKSERC721.minters(REDEEM.address)

    REDEEM.redeem(1, transact={'from': a0})
    assert SOCKSERC20.totalSupply() == 500 * 10**18 - 1
    assert SOCKSERC721.totalSupply() == 1

    assert_tx_failed(lambda: REDEEM.redeem(1, transact={'from': a0}))
    assert SOCKSERC20.totalSupply() == 500 * 10**18 - 1

    SOCKSERC20.approve(REDEEM.address, 1, transact={'from': a0})
    REDEEM.redeem(1, transact={'from': a0})
    assert SOCKSERC20.totalSupply() == 500 * 10**18 - 2
    assert REDEEM.tokensMinted() == 2


def test_redeem_several(w3, REDEEM, SOCKSERC20, SOCKSERC721, assert_tx_failed):
    a0, a1 = w3.eth.accounts[:2]
    SOCKSERC20.approve(REDEEM.address, 500, transact={'from': a0})
    SOCKSERC721.addMinter(REDEEM.address, transact={'from': a0})

    REDEEM.redeem(9, transact={'from': a0})
    assert REDEEM.tokensMinted() == 9
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
