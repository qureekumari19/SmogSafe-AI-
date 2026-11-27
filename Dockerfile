FROM nginx:alpine
COPY . /usr/share/nginx/html
RUN printf 'server {\n\
  listen 8080;\n\
  server_name _;\n\
  root /usr/share/nginx/html;\n\
  index index.html;\n\
  add_header X-Frame-Options "DENY" always;\
  add_header Cross-Origin-Opener-Policy "same-origin" always;\
  add_header Cross-Origin-Resource-Policy "same-origin" always;\n\
  add_header X-Content-Type-Options "nosniff" always;\n\
  add_header Referrer-Policy "strict-origin-when-cross-origin" always;\n\
  add_header Permissions-Policy "geolocation=(self), microphone=(), camera=()" always;\n\
  add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;\n\
  add_header Content-Security-Policy "default-src '\''self'\''; script-src '\''self'\'' '\''unsafe-inline'\'' '\''unsafe-eval'\'' https://cdn.tailwindcss.com https://ajax.googleapis.com; style-src '\''self'\'' '\''unsafe-inline'\'' https://fonts.googleapis.com; font-src '\''self'\'' https://fonts.gstatic.com; img-src '\''self'\'' data: blob:; connect-src '\''self'\'' https://vayu-saathi-460300800672.asia-south1.run.app; object-src '\''none'\''; base-uri '\''self'\''; frame-ancestors '\''none'\'';" always;\n\
  location / {\n\
    try_files $uri $uri/ /index.html;\n\
  }\n\
}\n' > /etc/nginx/conf.d/default.conf
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
