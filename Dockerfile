FROM docker.io/python:3.8-buster AS base

FROM base AS build

WORKDIR /work

COPY . .

RUN pip3 install pyinstaller

RUN pip3 install -r /work/requirements.txt
RUN pyinstaller --onefile /work/rssingle.py

FROM docker.io/python:3.8-buster AS app

COPY --from=build /work/dist/rssingle /rssingle

ENTRYPOINT ["/rssingle"]
