FROM --platform=linux/amd64 python:3.12

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

CMD ["fastapi", "run", "main.py", "--proxy-headers", "--port", "8080"]