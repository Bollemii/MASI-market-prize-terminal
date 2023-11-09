FROM docker:24.0.5

WORKDIR /app

COPY . /app/

RUN apk add make

CMD [ "make", "test" ]
