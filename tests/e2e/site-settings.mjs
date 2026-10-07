import { readSiteConfig } from '../../scripts/catalog/site-config.mjs';

export const settings = readSiteConfig();
export const port = Number(process.env.E2E_PORT || (settings.baseurl ? 4000 : 4173));
export const base = `http://127.0.0.1:${port}${settings.baseurl}/`;
export const baseurl = settings.baseurl;
export const siteOrigin = settings.origin;
export const siteDirectory = settings.siteDirectory;
