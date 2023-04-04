const algosdk = require('algosdk');

const kmd_token = 'a'.repeat(64);
const kmd_host = 'http://localhost';
const kmd_port = '4002';
const kmd_wallet = 'unencrypted-default-wallet';
const kmd_password = '';

const DefaultKMDConfig = {
  host: kmd_host,
  token: kmd_token,
  port: kmd_port,
  wallet: kmd_wallet,
  password: kmd_password,
};

exports.getAccounts = async function(
  config = DefaultKMDConfig,
) {
  const kmdClient = new algosdk.Kmd(config.token, config.host, config.port);

  const wallets = await kmdClient.listWallets();

  let walletId;
  for (const wallet of wallets['wallets']) {
    if (wallet['name'] === config.wallet) walletId = wallet['id'];
  }

  if (walletId === undefined) throw Error('No wallet named: ' + config.wallet);

  const handleResp = await kmdClient.initWalletHandle(
    walletId,
    config.password,
  );
  const handle = handleResp['wallet_handle_token'];

  const addresses = await kmdClient.listKeys(handle);
  const acctPromises = [];
  for (const addr of addresses['addresses']) {
    acctPromises.push(kmdClient.exportKey(handle, config.password, addr));
  }
  const keys = await Promise.all(acctPromises);

  // Don't need to wait for it
  kmdClient.releaseWalletHandle(handle);

  return keys.map((k) => {
    const addr = algosdk.encodeAddress(k.private_key.slice(32));
    const acct = { sk: k.private_key, addr: addr };
    const signer = algosdk.makeBasicAccountTransactionSigner(acct);
    return {
      addr: acct.addr,
      privateKey: acct.sk,
      signer: signer,
    };
  });
}

