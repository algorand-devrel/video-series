const algosdk = require('algosdk');
const {Buffer} = require("buffer");
const { getAccounts } = require('../sandbox');

const createAccount =  function (){
    try{  
        const myaccount = algosdk.generateAccount();
        console.log("Account Address = " + myaccount.addr);
        // the account address is derived from the public key
        let account_mnemonic = algosdk.secretKeyToMnemonic(myaccount.sk);
        // the mnemonic is a secret passphrase derived from the secret key        
        console.log("Account Mnemonic = "+ account_mnemonic);
        return myaccount;
    } catch (err) { console.log("err", err); }
};


async function firstTransaction() {

    try {

        let myAccount = createAccount();

        const algodToken = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
        const algodServer = 'http://localhost';
        const algodPort = 4001;

        let algodClient = new algosdk.Algodv2(algodToken, algodServer, algodPort);

        // fund newly created account
        const accts = await getAccounts();
        const fundingAcct = accts[0];
        const ptxn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
            from: fundingAcct.addr,
            to: myAccount.addr,
            amount: 10000000,
            suggestedParams: await algodClient.getTransactionParams().do(),
        })
        let {txId} = await algodClient.sendRawTransaction(ptxn.signTxn(fundingAcct.privateKey)).do();
        await algosdk.waitForConfirmation(algodClient, txId, 4)


        //Check your balance
        let accountInfo = await algodClient.accountInformation(myAccount.addr).do();
        console.log("Account balance: %d microAlgos", accountInfo.amount);
        let startingAmount = accountInfo.amount;

        // Construct the transaction
        const note = new Uint8Array(Buffer.from("Hello World"));
        let txn = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
            from: myAccount.addr,
            to: fundingAcct.addr,
            amount: 100000,
            suggestedParams: await algodClient.getTransactionParams().do(),
            note: note,
        });

        // Sign the transaction
        let signedTxn = txn.signTxn(myAccount.sk);
        txId = txn.txID().toString();
        console.log("Signed transaction with txID: %s", txId);

        // Submit the transaction
        await algodClient.sendRawTransaction(signedTxn).do();

        // Wait for confirmation
        //Get the completed Transaction
        let confirmedTxn = await algosdk.waitForConfirmation(algodClient, txId, 4);
        console.log("Transaction " + txId + " confirmed in round " + confirmedTxn["confirmed-round"]);

        let string = Buffer.from(confirmedTxn.txn.txn.note, 'base64').toString();
        console.log("Note field: ", string);

        accountInfo = await algodClient.accountInformation(myAccount.addr).do();
        console.log("Transaction Amount: %d microAlgos", confirmedTxn.txn.txn.amt);        
        console.log("Transaction Fee: %d microAlgos", confirmedTxn.txn.txn.fee);

        let closeoutamt = startingAmount - confirmedTxn.txn.txn.amt - confirmedTxn.txn.txn.fee;     
        console.log("Close To Amount: %d microAlgos", closeoutamt);
        console.log("Account balance: %d microAlgos", accountInfo.amount);
    }
    catch (err) {
        console.log("err", err);
    }
    process.exit();
};

firstTransaction();