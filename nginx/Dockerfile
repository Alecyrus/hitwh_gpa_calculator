FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf

ADD frontend.conf /etc/nginx/conf.d/
ADD backend.conf /etc/nginx/conf.d/