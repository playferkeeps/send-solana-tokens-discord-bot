const web3 = require("@solana/web3.js");
const { Token } = require("@solana/spl-token");


export default (async () => (
    async function generateWalletAndAirdrop() {
        // Generate a new wallet keypair and airdrop SOL
        var fromWallet = web3.Keypair.generate();
        var fromAirdropSignature = await connection.requestAirdrop(
            fromWallet.publicKey,
            web3.LAMPORTS_PER_SOL
        );
        // Wait for airdrop confirmation
        await connection.confirmTransaction(fromAirdropSignature);
    }

))();