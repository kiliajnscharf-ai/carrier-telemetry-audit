const express = require('express');
const axios = require('axios');
const { runCrawler } = require('./crawler');
const app = express();
app.use(express.json());
app.use(require('cors')());

app.get('/api/feed', async (req, res) => {
  const items = await runCrawler();
  res.json({ status: 'ok', items });
});

app.listen(3000, () => console.log('UpdateCheck API l??uft auf Port 3000'));
