const fetch = require('node-fetch');
const cheerio = require('cheerio');

async function crawl(url, tag) {
  try {
    const res = await fetch(url);
    const html = await res.text();
    const $ = cheerio.load(html);

    const items = [];

    $('h2, h3').each((i, el) => {
      const title = $(el).text().trim();
      if (!title) return;

      items.push({
        title,
        summary: "Auto summary placeholder",
        tag,
        source: url,
        time: Date.now()
      });
    });

    return items;
  } catch (err) {
    return [];
  }
}

async function runCrawler() {
  const feeds = [];

  const googleAI = await crawl("https://blog.google/technology/ai/", "Google AI");
  const android = await crawl("https://www.android.com/", "Android");
  const tech = await crawl("https://www.theverge.com/tech", "Tech");

  feeds.push(...googleAI);
  feeds.push(...android);
  feeds.push(...tech);

  return feeds;
}

module.exports = { runCrawler };
