import express from 'express';
import { sendToken } from '../sendtoken.js';
import bodyParser from 'body-parser'
const app = express()
const port = 42069
var jsonParser = bodyParser.json()
 
app.post('/send-token',jsonParser, (req, res) => {
    console.log(req.body)
    res.send(sendToken(req.body.symbol, req.body.amount, req.body.recepient));
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})