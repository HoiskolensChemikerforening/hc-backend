FROM nginx:1.11
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY sites-enabled/ /etc/nginx/sites-enabled
COPY custom_50x.html /www/errors/custom_50x.html
