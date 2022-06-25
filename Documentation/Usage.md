## Run

1. Download the binary.

**Linux**

``` shell
wget https://github.com/tanrax/RSSingle/releases/download/v1.0.0/rssingle
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