FROM ubuntu:24.04
RUN apt update && apt install -y ca-certificates curl git
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
RUN echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu noble stable" > /etc/apt/sources.list.d/docker.list
RUN apt update && apt install -y neovim docker-ce-cli docker-compose-plugin
ENV TERM=xterm-256color
