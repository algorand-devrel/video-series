const algosdk = require('algosdk');

async function recoverAccount() {
    try {
        // Generate a new account
        const account = algosdk.generateAccount()
        console.log("Generated account address: ", account.addr)
        // Get the mnemonic for it
        const passphrase = algosdk.mnemonicFromSeed(account.sk.slice(0, 32));
        // WARNING: never expose your mnemonic in a public repo
        console.log("Generated account mnemonic: ", passphrase);
        // Recover the account from the mnemonic
        const myRestoredAccount = algosdk.mnemonicToSecretKey(passphrase);
        console.log("Recovered account address: ", myRestoredAccount.addr);
    } catch (err) { console.log("err", err); }

};

recoverAccount();