# RSSingle

Generates an RSS file from the list of other feeds (RSS/Atom/JSON). Very handy when you want to centralise the list of your feeds in one place and all your devices feed from the same place.

## Run

1. Download the binary.

**Linux**

``` shell
curl -o rssingle https://github.com/tanrax/RSSingle/releases/download/v1.0.0/rssingle
```

**MacOS and Windows**

Coming soon

2. Gives execution permissions.

``` shell
chmod +x rssingle
```

3. In the same directory as the binary, you can create a local `config.yml` file in this format:

``` yaml
title: My RSS Feed
description: My customised RSS feed with technology news
url: https://www.example.com
output: rss.xml
feeds:
  - https://programadorwebvalencia.com/feed/
  - https://republicaweb.es/feed/
```

If not, you can download the example in the repository.

``` shell
curl -o config.yml https://raw.githubusercontent.com/tanrax/RSSingle/master/config.yml
```

4. Run the binary.

``` shell
./rssingle 
```

A file called `rss.xml` will be created.

## Development

### Compiling

```shell
pyinstaller --onefile rssingle.py
```

You will find the binary in `dist`.

## Thanks

@shymega for his original project [singlerss](https://github.com/shymega/singlerss).
