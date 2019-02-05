FROM python:3.5-alpine

RUN set -e; \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers;

# Expose the port uWSGI will listen on
EXPOSE 5000
RUN mkdir code
COPY requirements.txt /code
WORKDIR /code
# Install Python dependencies
RUN pip install -r requirements.txt
RUN pip install uWSGI==2.0.17.1

RUN apk del .build-deps;

COPY . .

# Run uwsgi from ini file
CMD [ "uwsgi", "--ini", "app.ini" ]