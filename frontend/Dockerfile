FROM nginx:latest
COPY default /etc/nginx/conf.d/default.conf
COPY rate_limit.conf /etc/nginx/conf.d/
COPY index.html /var/www/html/
CMD ["nginx", "-g", "daemon off;"]

