// @ts-check
import { defineConfig } from 'astro/config';
import fs from 'node:fs';
import path from 'node:path';

/**
 * Eine extrem robuste Sitemap-Integration.
 * @param {string} siteUrl - Die Basis-URL der Website.
 */
const customSitemap = (siteUrl) => ({
  name: 'custom-sitemap',
  hooks: {
    'astro:build:done': async ({ pages }) => {
      // Bereinige die URL (entferne trailing slash falls vorhanden)
      const cleanSiteUrl = siteUrl.endsWith('/') ? siteUrl.slice(0, -1) : siteUrl;

      // Erstelle den XML-Inhalt mit maximaler Sicherheit
      const sitemapContent = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  ${pages
    .filter(p => p && p.url) // Nur Seiten, die eine URL haben
    .map(p => {
      // Extrahiere den Pfad sicher (als String oder aus .href)
      const u = typeof p.url === 'string' ? p.url : (p.url && p.url.href);
      if (!u) return '';

      // Baue die vollständige URL
      const loc = u.startsWith('http') ? u : `${cleanSiteUrl}${u.startsWith('/') ? u : '/' + u}`;
      
      return `
  <url>
    <loc>${loc}</loc>
    <lastmod>${new Date().toISOString()}</lastmod>
  </url>`;
    }).join('')}
</urlset>`;

      const distDir = path.resolve(process.cwd(), 'dist');
      
      if (!fs.existsSync(distDir)) {
        console.error('Sitemap Error: dist directory not found at', distDir);
        return;
      }

      fs.writeFileSync(path.join(distDir, 'sitemap.xml'), sitemapContent);
      console.log('✅ Custom Sitemap successfully generated at dist/sitemap.xml');
    }
  }
});

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
  integrations: [customSitemap('https://rivieraandridge.com')],
});