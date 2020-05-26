# novelapp

## Setup
```
$ git clone git@github.com:tayutaedomo/novelapp.git
$ cd novelapp
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## git lfs
You have to execute the following commands as use git lfs.
```
$ git lfs install
```

## Scraping Execution
1. Create syuppan.csv
```
$ python scripts/scraping/narou_syuppan.py
```

2. Create novels.csv
```
$ python scripts/scraping/narou_syuppan_novelview.py
```

3. Download images
```
$ python scripts/scraping/narou_syuppan_images.py
```

## Local Server
```
$ cd flask-sandbox
$ python app.py
$ open "http://localhost:5000/"
```
Basic Auth: novelapp / novels

## Config ENV
You should set the appropriate ENV.
```
$ export APP_SETTINGS="config.DevelopmentConfig"
# or
$ export APP_SETTINGS=config.StagingConfig
# or
$ export APP_SETTINGS=config.ProductionConfig
```

