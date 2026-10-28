# Khiangte Villain portfolio

A static GitHub Pages portfolio and Prompt Vault. It uses plain HTML, CSS, and browser JavaScript—there is no server, account system, build step, database, API client, or credential.

## Architecture

- `index.html` is the only page entry point.
- `styles.css` provides the site styling.
- `script.js` contains the in-browser Prompt Vault filtering, copy, and share behavior.
- `hero-bike.png`, `favicon.png`, and `prompt-packs/` are the published local assets.

The Prompt Vault is fully client-side. It never sends prompt content to a backend. Copy uses the browser Clipboard API with a local fallback; Share uses the Web Share API with the same copy fallback.

## Deployment

GitHub Pages is deployed through [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) on pushes to `main` or manual runs. The workflow creates a temporary `_site` directory and uploads only:

- `index.html`
- `styles.css`
- `script.js`
- `favicon.png`
- `hero-bike.png`
- `prompt-packs/`

In **Settings → Pages**, set the source to **GitHub Actions**. Do not use “Deploy from a branch”; the root contains repository files that are not part of the published site.

## Security model

No secret belongs in this repository or static Pages deployment. The site contains no Gemini, Google, or other API key, and the Pages workflow does not read or inject secrets.

If a Gemini key was used by an earlier deployment, rotate or revoke it in Google AI Studio / Google Cloud and remove the obsolete `API_KEY` Actions secret from this repository. Historical Pages artifacts and prior deployments should be treated as potentially exposed until that credential is rotated.

## Local preview

Open `index.html` in a browser. For Clipboard API behavior closest to production, serve the folder from a local web server rather than opening it with a `file:` URL.
