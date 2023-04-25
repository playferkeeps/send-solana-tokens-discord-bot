import express from 'express';
import { sendToken } from '../sendtoken.js';
const app = express()
const port = 42069

app.post('/send-token', (req, res) => {
    res.send(sendToken('SPA'));
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})