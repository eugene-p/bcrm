FROM nginx:1.15.8

EXPOSE 80

RUN rm /etc/nginx/conf.d/default.conf

# import nginx config
COPY nginx.conf /etc/nginx/conf.d