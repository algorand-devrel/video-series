const algosdk = require("algosdk");
const {AtomicTransactionComposer } = require("algosdk");

const faucet_addr = "GD64YIY3TWGDMCNPP553DZPPR6LDUSFQOIJVFDPPXWEG3FVOJCCDBBHU5A"
// TestNet
const token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const server = "http://localhost";
const port = 4001;


const client = new algosdk.Algodv2(token, server, port);
const txids = [];

function recoverAccount1() {
    // const passphrase = "Your 25-word mnemonic goes here";
    const passphrase = "price clap dilemma swim genius fame lucky crack torch hunt maid palace ladder unlock symptom rubber scale load acoustic drop oval cabbage review abstract embark";
    let myAccount = algosdk.mnemonicToSecretKey(passphrase);
    return myAccount;
}
// recover second account
function recoverAccount2() {
    // const passphrase = "Your 25-word mnemonic goes here";
    const passphrase = "unlock garage rack news treat bonus census describe stuff habit harvest imitate cheap lemon cost favorite seven tomato viable same exercise letter dune able add";
    let myAccount = algosdk.mnemonicToSecretKey(passphrase);
    return myAccount;
}

(async function () {
  try {
    let myAccountA = await recoverAccount1();
    console.log("My account A address: %s", myAccountA.addr)

    // recover an additional account
    // Account B
    let myAccountB = await recoverAccount2();
    console.log("My account B address: %s", myAccountB.addr)


    let accountInfo = await client.accountInformation(myAccountA.addr).do();
    console.log("Account A balance: %d microAlgos", accountInfo.amount);
    accountInfo = await client.accountInformation(myAccountB.addr).do();
    console.log("Account B balance: %d microAlgos", accountInfo.amount); 


    // Construct a `signer` object that will be used to sign transactions
    // later the during AtomicTransactionComposer group transaction construction
    // process
    const signer = algosdk.makeBasicAccountTransactionSigner(myAccountA) 

    // AtomicTransactionComposer allows us to easily add transactions
    // and ABI method calls to construct an atomic group
    const atc = new AtomicTransactionComposer()

    // Get the suggested parameters from the Algod server. 
    // These include current fee levels and suggested first/last rounds.
    const sp = await client.getTransactionParams().do();

    // Send .1 Algo to the faucet address
    const txn1 = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
      from: myAccountA.addr, 
      to: faucet_addr,
      amount: 100000,
      suggestedParams: sp,
    });
    atc.addTransaction({ txn: txn1, signer: signer })

        // Send .2 Algo to AccountB
    const txn2 = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
        from: myAccountA.addr, 
        to: myAccountB.addr,
        amount: 200000,
        suggestedParams: sp,
        });
        atc.addTransaction({ txn: txn2, signer: signer })



    // Send the transaction, returns the transaction id for 
    // the first transaction in the group
    const results = await atc.execute(client, 2);

    console.log("Confirmed in round: ", results.confirmedRound)

    //Get the completed Transactions
    console.log("Transaction 1 " + results.txIDs[0] + " confirmed in round " + results.confirmedRound);
    console.log("Transaction 2 " + results.txIDs[1] + " confirmed in round " + results.confirmedRound);
    console.log("Group ID = " + new Buffer.from(txn2.group).toString('base64') );
    
   
    accountInfo = await client.accountInformation(myAccountA.addr).do();
    console.log("Account A balance: %d microAlgos", accountInfo.amount);
    accountInfo = await client.accountInformation(myAccountB.addr).do();
    console.log("Account B balance: %d microAlgos", accountInfo.amount);  
 
  } catch (error) {
    console.log("err", error);
    // printError(error);
    return;
  }


})();