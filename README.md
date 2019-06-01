
## Tomori Nao

Basic Discord bot that pings you when a new anime episode or manga chapter is released, based on your [MyAnimeList](https://myanimelist.net/) account. I couldn't find any bot that does this, so I wrote one my own.
And yes, Tomori Nao is my waifu.

This is just a personal bot, meaning it only servers one user at a time, so feel free to use it for yourself.

## Setup

Before running setting up, make sure you are using python3.7.

```bash
pip install -r requirements.txt
export DISCORD_CLIENT_TOKEN=<TOKEN>
python main.py
```

Alternatively, you can [Heroku](https://www.heroku.com/) to host the discord bot for free, there are already config files present, so the deployment should be easy.

## Tests

Run all unit tests:
```bash
python -m unittest -v
```
