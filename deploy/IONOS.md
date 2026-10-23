# IONOS Ubuntu deployment files

These files target the Ubuntu/Nginx host at `87.106.214.100` and serve the frontend on `alpha.flexhappyhours.com`. The Nginx site serves `FRONTENT/dist` and proxies the app API and uploaded assets to FastAPI on `127.0.0.1:8000`.

## Before enabling the site

1. Confirm the domain's A record remains pointed at `87.106.214.100`; DNS currently resolves to this IP.
2. Install the project under `/opt/flexhappyhours`; install Node.js/npm, Python 3 with venv support, Nginx, MySQL, and Certbot's Nginx plugin.
3. Create a production database and a dedicated database user. Set `DATABASE_URL` and `AGENT_DATABASE_URL` in `/opt/flexhappyhours/.env`, along with any optional provider keys. Use newly generated credentials; do not reuse credentials found in the Git history. Keep `.env` private and readable only by the service account.
4. From the project root, create `.venv`, install `requirements.txt`, and install frontend dependencies from `FRONTENT/package-lock.json` with `npm ci`. Build the frontend with the default production API prefix `/api`; Nginx removes this prefix and proxies requests to FastAPI on the same host. Set `VITE_API_BASE_URL` only if the API is hosted elsewhere.
5. Install `flexhappyhours-api.service` under `/etc/systemd/system/`, then enable and start it with systemd.
6. Install `ionos-nginx.conf` under `/etc/nginx/sites-available/`, enable it, validate Nginx configuration, and reload Nginx.
7. Issue and install the TLS certificate with Certbot for `alpha.flexhappyhours.com`. HTTPS is required for browser geolocation.

The API creates its SQLAlchemy tables on startup, but this does not migrate an existing database schema. Back up any existing production data before changing the live site.
