import express from 'express';
import { sendToken } from '../sendtoken.js';
import bodyParser from 'body-parser'
const app = express()
const port = 42069
var jsonParser = bodyParser.json()

app.post('/send-token-to-address', jsonParser, async (req, res) => {
    console.log(req.body)
    try {
        const sig = await sendToken(req.body.symbol, req.body.amount, req.body.recepient);
        res.send({ "success": "true", "tx_signature": `${sig}` });
    } catch (e) {
        res.send({ "success": "false" });
    }
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})