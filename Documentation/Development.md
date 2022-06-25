## Development

### Compiling

```shell
pyinstaller --onefile rssingle.py
```

Old versions

```shell
docker run --rm --volume $PWD:/app python:3.8-buster /bin/bash -c "cd /app; pip3 install -r requirements.txt; pyinstaller --onefile rssingle.py"
```

You will find the binary in `dist`.