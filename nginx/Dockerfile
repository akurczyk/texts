FROM nginx:1.17.5-alpine
RUN rm /etc/nginx/conf.d/default.conf && \
    rm /usr/share/nginx/html/50x.html && \
    rm /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/conf.d
