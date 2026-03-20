FROM nginx:latest
COPY default /etc/nginx/conf.d/default.conf
COPY index.html /var/www/html/
CMD ["nginx", "-g", "daemon off;"]

