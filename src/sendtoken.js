import { clusterApiUrl, Connection, Keypair, Transaction, PublicKey, sendAndConfirmTransaction } from '@solana/web3.js';
import { getOrCreateAssociatedTokenAccount, createTransferInstruction } from '@solana/spl-token';
import secret from './mint_key.json' assert { type: "json" };
import tokens from './static/tokens.json' assert { type: "json" };
const DEV_ACCOUNT = 'BHXso3QjGLbYKX94ULvj8YpHYSd2B9kEoFTARX8dZFt1';

async function getNumberDecimals(mintAddress, connection) {
    const info = await connection.getParsedAccountInfo(new PublicKey(mintAddress));
    const result = (info.value.data).parsed.info.decimals;
    return result;
}

async function collectTax(taxAmt, tokenAmt) {
    return tokenAmt * taxAmt; //0.5% tax of whatever token, sent to dev
}

async function addTransaction(transaction, sourceTokenAccountAddress, destTokenAccountAddress, ownerAddress, amount) {
    transaction.add(createTransferInstruction(
        sourceTokenAccountAddress,
        destTokenAccountAddress,
        ownerAddress,
        amount
    ))
}

export async function sendToken(tokenSymbolOrAddress, amountToSend, recipient) {
    const tokenResult = tokens.filter(token => {
        return (token.mintAddress == tokenSymbolOrAddress || token.symbol == tokenSymbolOrAddress)
    })
    if (tokenResult == []) {
        return 'NOT SUPPORTED.'
    }

    const token = tokenResult[0];
    console.log(token)

    const mintAddress = token.mintAddress;
    // Connect to cluster
    const connection = new Connection(clusterApiUrl('devnet'), 'confirmed');
    // Generate a new wallet keypair and airdrop SOL
    const fromWallet = Keypair.fromSeed(new Uint8Array([10, 46, 82, 157, 49, 183, 154, 88, 228, 193, 30, 79, 38, 73, 77, 123, 20, 0, 222, 57, 42, 67, 56, 196, 76, 57, 157, 50, 183, 6, 64, 145, 46, 207, 139, 155, 227, 60, 164, 220, 86, 165, 184, 216, 48, 179, 187, 252, 243, 114, 79, 70, 122, 136, 240, 70, 242, 146, 9, 102, 87, 188, 22, 46].slice(0, 32)))
    const toWallet = new PublicKey(recipient)
    const tax = await collectTax(0.005, amountToSend);
    console.log(`receivingWalletPublicKey: ${toWallet}`)
    console.log(`amountToSend: ${amountToSend}`)

    // Get the token account of the fromWallet address, and if it does not exist, create it
    const fromTokenAccount = await getOrCreateAssociatedTokenAccount(
        connection,
        fromWallet,
        new PublicKey(mintAddress),
        fromWallet.publicKey
    );

    // Get the token account of the toWallet address, and if it does not exist, create it
    const toTokenAccount = await getOrCreateAssociatedTokenAccount(connection, fromWallet, new PublicKey(mintAddress), toWallet);
    const devAccount = await getOrCreateAssociatedTokenAccount(connection, fromWallet, new PublicKey(mintAddress), new PublicKey(DEV_ACCOUNT));

    // Mint 1 new token to the "fromTokenAccount" account we just created
    const tx = new Transaction();
    addTransaction(tx,
        fromTokenAccount.address,
        toTokenAccount.address,
        fromWallet.publicKey,
        amountToSend * Math.pow(10, token.decimals))

    console.log('sent user')
    console.log(`tax ${tax}`)

    //Pay dev
    addTransaction(tx,
        fromTokenAccount.address,
        devAccount.address,
        fromWallet.publicKey,
        Math.floor(tax) * Math.pow(10, token.decimals))

    console.log('sent dev')
    const latestBlockHash = await connection.getLatestBlockhash('confirmed');
    tx.recentBlockhash = await latestBlockHash.blockhash;
    const signature = await sendAndConfirmTransaction(connection, tx, [fromWallet]);
    console.log(
        '\x1b[32m', //Green Text
        `Transaction Success!🎉 ${amountToSend} ${token.symbol} Sent!`,
        `\n  https://solscan.io/tx/${signature}?cluster=devnet`
    );

    console.log(`dev collected: ${tax} $${token.symbol}`)
    return signature
}

export default {
    sendToken
}