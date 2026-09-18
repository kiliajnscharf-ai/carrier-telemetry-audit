const express = require('express');
const { runCrawler } = require('./crawler');
const app = express();
app.use(express.json());
app.use(require('cors')());

app.get('/api/feed', async (req, res) => {
  try {
    const items = await runCrawler();
    res.json({ status: 'ok', items });
  } catch (err) {
    res.json({ status: 'error', items: [], error: err.message });
  }
});

app.listen(3000, () => console.log('UpdateCheck API läuft auf Port 3000'));
