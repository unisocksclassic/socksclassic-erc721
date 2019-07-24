# @dev Redeem Socksclassic ERC20 for NFT

# Interface for ERC721 contract
contract SocksERC721:
    def mint(_to: address, _tokenId: uint256) -> bool: modifying

# Interface for ERC20 contract
contract SocksERC20:
    def burnFrom(_from: address, _value: uint256) -> bool: modifying

# @dev This emits when the holder of erc20 token is burning his token and minting a new NFT
# @param _owner Owner of NFT.
# @param _tokenId NFT which we are approving.
Redemption: event({
        _owner: indexed(address),
        _tokenId: indexed(uint256)
    })

token: public(SocksERC20)
nft: public(SocksERC721)
tokensMinted: public(uint256)
owner: public(address)
startingIndex: uint256

@public
def __init__(_erc20: address, _erc721: address):
    """
    @dev Contract constructor.
    @param _erc20 Address of erc20 token to burn on redeem call
    @param _erc721 NFT Token to mint
    """
    self.token = SocksERC20(_erc20)
    self.nft = SocksERC721(_erc721)
    self.owner = msg.sender

@public
def redeem(_value: uint256) -> bool:
    """
    @dev Function to redeem tokens
    @param _value Amount of erc20 tokens to redeem
    """
    assert _value != 0
    self.token.burnFrom(msg.sender, _value*10**18)

    for i in range(90):
      if convert(i, uint256) >= _value:
        break

      token_id: uint256 = self.tokensMinted + self.startingIndex +  convert(i, uint256)
      self.nft.mint(msg.sender, token_id)
      log.Redemption(msg.sender, token_id)


    self.tokensMinted += _value

    return True
  
@public
def change_token_address(_address: address):
    assert msg.sender == self.owner
    self.token = SocksERC20(_address)
  
@public
def change_nft_address(_address: address):
    assert msg.sender == self.owner
    self.nft = SocksERC721(_address)

@public
def changeOwner(_owner: address):
    assert _owner != ZERO_ADDRESS
    assert self.owner == msg.sender
    self.owner = _owner

@public
def setStartingIndex(_index: uint256):
    assert self.owner == msg.sender
    self.startingIndex = _index
