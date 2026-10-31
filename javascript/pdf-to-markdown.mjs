// Convert a PDF to Markdown with the Document to Markdown Actor.
// Usage: APIFY_TOKEN=... node pdf-to-markdown.mjs https://arxiv.org/pdf/1706.03762
import { ApifyClient } from 'apify-client';

const urls = process.argv.slice(2);
const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor('caspiandata/doc-to-markdown').call({
    urls: urls.length ? urls : ['https://arxiv.org/pdf/1706.03762'],
    pageRange: '1-3',
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const doc of items) {
    if (doc.error) { console.error(`Skipped ${doc.sourceUrl}: ${doc.error}`); continue; }
    console.log(`# ${doc.title} — ${doc.processedPages} pages, ${doc.chunks.length} chunks\n`);
    console.log(doc.markdown.slice(0, 1000));
}
