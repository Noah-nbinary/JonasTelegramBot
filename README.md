Environment Variables:
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
TELEGRAM_BOT_NAME=YOUR_BOT_NAME

Sample Docker Compose:
services:
  
  provider-bot:
    image: noahnbinary/provider-bot:trixie
    container_name: provider-bot
    restart: always
    env_file:
      - .env