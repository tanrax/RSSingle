#!/usr/bin/env python3

# Copyright (c) Dom Rodriguez 2020
# Copyright (c) Andros Fenollosa 2022
# Licensed under the Apache License 2.0

import os
import sys
import feedparser
import logging
import listparser
from os import environ
from feedgen.feed import FeedGenerator
import json
import yaml


# Variables

log = None
CONFIG_PATH = "config.yml"
LOG_LEVEL = environ.get("SR_LOG_LEVEl", "ERROR")
fg = None
FEED_OUT_PATH = None
FEEDS = []
CFG = None


def setup_logging() -> None:
    """
    This function intiialises the logger framework.
    """
    global log

    log = logging.getLogger(__name__)
    log.setLevel(LOG_LEVEL)
    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(LOG_LEVEL)
    ch.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    log.addHandler(ch)

    return None


def get_url_from_feed(config) -> str:
    """
    This function returns the URL from a feed.
    """
    return config["url"] + "/" + config["output"]


def init_feed() -> None:
    """
    This function initialises the RSS feed with the
    correct attributes.
    """
    log.debug("Initialising the feed...")

    global fg

    try:
        fg = FeedGenerator()
        # Setup [root] feed attributes
        fg.id(get_url_from_feed(CONFIG))
        fg.title(CONFIG["title"])
        fg.generator("RSSingle/v1.0.0")
        fg.link(href=get_url_from_feed(CONFIG), rel="self")
        fg.subtitle(CONFIG["description"])
        fg.language("en")
    except BaseException: # find out what exceptions FeedGenerator can cause as well as KeyError.
        logging.exception("Error initialising the feed!")

    log.debug("Feed initialised!")

    return None


def parse_rss_feed(url) -> feedparser.FeedParserDict:
    log.debug("Parsing RSS feed..")

    try:
        # Hopefully this should parse..
        return feedparser.parse(url)
    except BaseException: # find out what exceptions .parse() call can cause.
        log.warning("Failed to parse RSS feed.")
        # Now, we could handle gracefully.

def filter_feed_entries(entry) -> bool:
    """
    This function filters feed entries based on strings defined in config.yml.
    """
    filter_strings = CONFIG.get("filter_strings", [])
    for filter_str in filter_strings:
        if filter_str.lower() in entry.get("title", "").lower() or filter_str.lower() in entry.get("summary", "").lower():
            log.debug(f"Entry filtered out: {entry['title']}")
            return False
    return True

def main():
    log.debug("Loading feed list into memory..")

    log.debug("Iterating over feed list..")

    for feed in CONFIG["feeds"]:
        rss = parse_rss_feed(feed)
        entries = rss.get("entries")
        log.debug("Iterating over [input] feed entries..")
        for entry in entries[:CONFIG["max_entries"]] if "max_entries" in CONFIG else entries:
            log.debug("New feed entry created.")

            if not filter_feed_entries(entry):
                continue  # Skip this entry

            fe = fg.add_entry()

            log.debug("Working on new feed entry..")


            try:
                fe.id(entry["id"])
            except KeyError:
                # Definitely weird...
                log.warning("Empty id attribute, defaulting..")
                fe.id("about:blank")

            try:
                fe.title(entry["title"])
            except KeyError:
                # OK, this is a definite malformed feed!
                log.warning("Empty title attribute, defaulting..")
                fe.title("Unspecified")

            try:
                fe.link(href=entry["link"])
            except KeyError:
                # When we have a empty link attribute, this isn't ideal
                # to set a default value.. :/
                log.warning("Empty link attribute, defaulting..")
                fe.link(href="about:blank")

            try:
                if entry["sources"]["authors"]:
                    for author in entry["sources"]["authors"]:
                        fe.author(author)
                elif entry["authors"]:
                    try:
                        for author in entry["authors"]:
                            fe.author(author)
                    except KeyError:
                        log.debug("Oh dear, a malformed feed! Adjusting.")
                        # This is a ugly hack to fix broken feed entries with the author attribute!
                        author["email"] = author.pop("href")
                        fe.author(author)
            except KeyError:
                # Sometimes we don't have ANY author attributes, so we
                # have to set a dummy attribute.
                log.warning("Empty authors attribute, defaulting..")
                fe.author({"name": "Unspecified", "email": "unspecified@example.com"})

            try:
                if entry["summary"]:
                    fe.summary(entry["summary"])
                    fe.description(entry["summary"])
                elif entry["description"]:
                    fe.description(entry["description"])
                    fe.summary(entry["description"])
                    fe.content(entry["description"])
            except KeyError:
                # Sometimes feeds don't provide a summary OR description, so we
                # have to set an empty value.
                # This is pretty useless for a feed, so hopefully we
                # don't have to do it often!
                log.warning("Empty description OR summary attribute, defaulting..")
                fe.description("Unspecified")
                fe.summary("Unspecified")

            try:
                if entry["published"]:
                    try:
                        fe.published(entry["published"])
                        fe.updated(entry["published"])
                    except KeyError:
                        fe.published("1970-01/01T00:00:00+00:00")
                        fe.updated("1970-01/01T00:00:00+00:00")
                        continue
            except Exception:
                # Sometimes feeds don't even provide a publish date, so we default to
                # the start date &time of the Unix epoch.
                log.warning("Empty publish attribute, defaulting..")
                fe.published("1970-01/01T00:00:00+00:00")
                fe.updated("1970-01/01T00:00:00+00:00")


if __name__ == "__main__":
    setup_logging()
    log.debug("Initialising...")

    global CONFIG

    with open("config.yml", "r") as file:
        CONFIG = yaml.safe_load(file)

    log.debug("Assiging variables..")
    try:
        # Configuration is specified with configure variables.
        log.debug("Assignment attempt: output")
        FEED_OUT_PATH = CONFIG["output"]
    except KeyError:
        log.error("*** Configure variable missing! ***")
        log.error("`output` variable missing.")
        log.error("This program will NOT run without that set.")
        sys.exit(1)

    init_feed()

    log.debug("Begin processing feeds...")
    main()

    fg.rss_file(FEED_OUT_PATH)
