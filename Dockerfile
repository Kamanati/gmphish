FROM debian:latest
LABEL MAINTAINER="https://github.com/Kamanati/gmphish"

WORKDIR /gmphish/
ADD . /gmphish 

RUN apt update && \
    apt full-upgrade -y && \
    apt install -y curl unzip wget && \
    apt install --no-install-recommends -y php && \
    apt clean
CMD ["./start.sh"]
