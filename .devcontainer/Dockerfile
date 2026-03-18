FROM ubuntu:24.04
RUN  apt update
RUN  apt install -y neovim python3 python3-pip git nginx curl
ENV TERM=xterm-256color
RUN python3 -m pip install "fastapi[standard]" --break-system-packages
RUN rm -f /etc/nginx/sites-enabled/default
COPY default /etc/nginx/sites-enabled/
