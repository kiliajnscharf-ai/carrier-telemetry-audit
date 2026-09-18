#!/usr/bin/env node
const axios = require('axios');

async function main() {
  const mode = process.argv[2] || 'feed';

  if (mode === 'feed') {
    const res = await axios.get('http://localhost:3000/api/feed');
    console.log("UpdateCheck Feed:");
    res.data.items.forEach((item) => {
      console.log("-----");
      console.log("Titel:", item.title);
      console.log("Tag:", item.tag);
      console.log("Quelle:", item.source);
    });
  } else {
    console.log("Unbekannter Modus:", mode);
  }
}

main().catch(err => {
  console.error("Fehler:", err.message);
  process.exit(1);
});
