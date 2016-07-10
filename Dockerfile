FROM ubuntu:latest

# Update and install packages
RUN apt-get update -y
RUN apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    libpq-dev \
    nginx \
    supervisor

# Make NGINX run on the foreground
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
# Remove default configuration from Nginx
RUN rm /etc/nginx/sites-enabled/default

COPY src/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt uwsgi -U

COPY root /
RUN ln -s /etc/nginx/sites-available/server.conf /etc/nginx/sites-enabled/
RUN mkdir /var/log/supervisord && chown www-data:www-data /var/log/supervisord

COPY src /app/

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

EXPOSE 80
