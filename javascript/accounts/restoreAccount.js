const algosdk = require('algosdk');

// Create an account and add funds to it. Copy the address off
// The Algorand TestNet Dispenser is located here: 
// https://dispenser.testnet.aws.algodev.network/

const restoreAccount =  function (){
    try{  

        // const passphrase = "Your 25-word mnemonic goes here";
        // never use mnemonics in code, for demo purposes only
        const passphrase = "price clap dilemma swim genius fame lucky crack torch hunt maid palace ladder unlock symptom rubber scale load acoustic drop oval cabbage review abstract embark";
        // restore the account from the passphrase        
        let myaccount = algosdk.mnemonicToSecretKey(passphrase);

  
        return myaccount;
    }
    catch (err) {
        console.log("err", err);
    }
};


async function firstTransaction() {

    try {
        let myAccount = restoreAccount();
        // the account address is derived from the public key
        console.log("Account Address = " + myAccount.addr);
     }
    catch (err) {
        console.log("err", err);
    }
    process.exit();
};

firstTransaction();