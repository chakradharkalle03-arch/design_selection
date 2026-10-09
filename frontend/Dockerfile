FROM caddy:2-alpine
COPY frontend/dist /usr/share/caddy
COPY frontend/Caddyfile /etc/caddy/Caddyfile

EXPOSE 80
CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]
