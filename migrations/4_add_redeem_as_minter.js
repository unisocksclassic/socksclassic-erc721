var RedeemContract = artifacts.require("redeemcontract");
var SocksClassic = artifacts.require("socksclassic");

module.exports = async function(deployer) {
  const socksClassic = await SocksClassic.deployed()
  await socksClassic.addMinter(RedeemContract.address)
};
