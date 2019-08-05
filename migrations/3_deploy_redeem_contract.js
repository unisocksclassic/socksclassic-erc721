var RedeemContract = artifacts.require("redeemcontract");
var SocksClassic = artifacts.require("socksclassic");

module.exports = async function(deployer) {
  const erc20address = '0xf7a5a8a95491ec170738434963b649671b563b88'
  const erc721address = SocksClassic.address;
  deployer.deploy(RedeemContract, erc20address, erc721address);
};
