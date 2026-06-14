// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://rivieraandridge.com',
  compressHTML: true,
  build: {
    inlineStylesheets: 'auto',
  },
  image: {
    domains: [],
  },
  integrations: [sitemap()],
});
