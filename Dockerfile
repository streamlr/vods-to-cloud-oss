FROM python:alpine3.21

WORKDIR /app

ENV TWITCH_CLIENT_ID=${TWITCH_CLIENT_ID}
ENV TWITCH_CLIENT_SECRET=${TWITCH_CLIENT_SECRET}
ENV TWITCH_REDIRECT_URI=${TWITCH_REDIRECT_URI}

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
