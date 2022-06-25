
# Development

<br>

## Compiling

*Commands are run from within the  `/Source/`  folder.*

<br>

```shell
pyinstaller --onefile rssingle.py
```
<br>

### Old Versions

```shell
docker run              \
    --rm                \
    --volume $PWD:/app  \
    python:3.8-buster   \
    /bin/bash -c        \
    "cd /app; pip3 install -r requirements.txt; pyinstaller --onefile rssingle.py"
```

<br>

You will find the binary in `/dist/`.

<br>