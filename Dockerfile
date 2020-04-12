FROM python:3

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1

COPY . /app

RUN pip install -r /app/pip.txt

CMD [ "python", "/app/app.py" ]