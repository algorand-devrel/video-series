const algosdk = require("algosdk");
const { AtomicTransactionComposer } = require("algosdk");
const { getAccounts } = require("../sandbox");


(async function () {
  try {

    const token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
    const server = "http://localhost";
    const port = 4001;

    const client = new algosdk.Algodv2(token, server, port);

    const accts = await getAccounts();

    const myAccountA = accts[0]
    console.log("My account A address: %s", myAccountA.addr)

    const myAccountB = accts[1];
    console.log("My account B address: %s", myAccountB.addr)



    let accountInfo = await client.accountInformation(myAccountA.addr).do();
    console.log("Account A balance: %d microAlgos", accountInfo.amount);

    accountInfo = await client.accountInformation(myAccountB.addr).do();
    console.log("Account B balance: %d microAlgos", accountInfo.amount);


    // Construct a `signer` object that will be used to sign transactions
    // later the during AtomicTransactionComposer group transaction construction
    // process
    const signerA = algosdk.makeBasicAccountTransactionSigner({addr: myAccountA.addr, sk:myAccountA.privateKey})
    const signerB = algosdk.makeBasicAccountTransactionSigner({addr: myAccountB.addr, sk: myAccountB.privateKey})

    // AtomicTransactionComposer allows us to easily add transactions
    // and ABI method calls to construct an atomic group
    const atc = new AtomicTransactionComposer()

    // Get the suggested parameters from the Algod server. 
    // These include current fee levels and suggested first/last rounds.
    const sp = await client.getTransactionParams().do();

    // Send .1 Algo from B to A 
    const txn1 = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
      from: myAccountB.addr,
      to: myAccountA.addr,
      amount: 100000,
      suggestedParams: sp,
    });
    atc.addTransaction({ txn: txn1, signer: signerB })

    // Send .2 Algo from A to B 
    const txn2 = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
      from: myAccountA.addr,
      to: myAccountB.addr,
      amount: 200000,
      suggestedParams: sp,
    });
    atc.addTransaction({ txn: txn2, signer: signerA })



    // Send the transaction, returns the transaction id for 
    // the first transaction in the group
    const results = await atc.execute(client, 2);

    console.log("Confirmed in round: ", results.confirmedRound)

    //Get the completed Transactions
    console.log("Transaction 1 " + results.txIDs[0] + " confirmed in round " + results.confirmedRound);
    console.log("Transaction 2 " + results.txIDs[1] + " confirmed in round " + results.confirmedRound);
    console.log("Group ID = " + new Buffer.from(txn2.group).toString('base64'));


    accountInfo = await client.accountInformation(myAccountA.addr).do();
    console.log("Account A balance: %d microAlgos", accountInfo.amount);
    accountInfo = await client.accountInformation(myAccountB.addr).do();
    console.log("Account B balance: %d microAlgos", accountInfo.amount);

  } catch (error) {
    console.error("err", error);
    return;
  }


})();