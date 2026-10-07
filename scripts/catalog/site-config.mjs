import fs from 'node:fs';
import path from 'node:path';
import { parse } from 'yaml';
import { ROOT } from './lib.mjs';

export function readSiteConfig({ root = ROOT, configPaths = process.env.JEKYLL_CONFIG || '_config.yml' } = {}) {
  const config = {};
  for (const file of configPaths.split(',')) {
    Object.assign(config, parse(fs.readFileSync(path.resolve(root, file.trim()), 'utf8')) || {});
  }
  return {
    configPaths,
    origin: new URL(config.url).origin,
    baseurl: config.baseurl || '',
    siteDirectory: path.resolve(root, config.destination || '_site'),
    reportDirectory: config.audit_report_directory || 'docs/audit',
    externalFonts: config.external_fonts !== false,
  };
}

export function legacySitePath(pathname) {
  const prefix = '/prompt-context-patterns';
  if (pathname === prefix) return '/';
  return pathname.startsWith(prefix + '/') ? pathname.slice(prefix.length) : pathname;
}
