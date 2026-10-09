from nginx
copy ./dist /usr/share/nginx/html
copy docker/static /static/
copy docker/nginx.conf /etc/nginx/conf.d/default.conf


expose 80
expose 443
copy docker/entrypoint.sh /entrypoint.sh
run chmod +x /entrypoint.sh

cmd ["/entrypoint.sh"]


