# novelapp-model

## Setup
```
$ git clone git@github.com:tayutaedomo/novelapp-model.git
$ cd novelapp-model
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```


## git lfs
You have to execute the following commands as use git lfs.
```
$ git lfs install
```


## Scraping Commands
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

4. Image Categorizing
```
$ python scripts/scraping/images_categorizing_copy.py
```

