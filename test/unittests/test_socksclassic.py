from test.constants import (
    DECIMALS,
    ZERO_ADDRESS,
    ERC165_INTERFACE_ID,
    ERC721_INTERFACE_ID, )


def test_init(w3, SOCKSERC721):
    a0, a1 = w3.eth.accounts[:2]
    assert SOCKSERC721.name() == 'Digital Unisocks Classic Edition 0'
    assert SOCKSERC721.symbol() == 'SOCKSCLASSIC'
    assert SOCKSERC721.totalSupply() == 0
    assert SOCKSERC721.minters(a0)
    assert SOCKSERC721.balanceOf(a1) == 0
    assert SOCKSERC721.supportsInterface(ERC165_INTERFACE_ID) is True
    assert SOCKSERC721.supportsInterface(ERC721_INTERFACE_ID) is True


def test_change_minter(w3, SOCKSERC721):
    a0, a1 = w3.eth.accounts[:2]
    assert SOCKSERC721.minters(a0)
    assert SOCKSERC721.addMinter(a1, transact={'from': a0, 'gas': 1000000})
    assert SOCKSERC721.minters(a1)


def test_change_minter_zero(w3, SOCKSERC721, assert_tx_failed):
    a0, a1 = w3.eth.accounts[:2]
    assert SOCKSERC721.minters(a0)
    SOCKSERC721.addMinter(
        a1, transact={
            'from': a0,
        })
    assert SOCKSERC721.minters(a1)


def test_get_token_uri(w3, SOCKSERC721):
    assert SOCKSERC721.tokenURI(
        0
    ) == 'https://cloudflare-ipfs.com/ipfs/QmVetwS6nt9ng9kFVStskZ1bmKWww42upDQHmSGqajbdrj'
