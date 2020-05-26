# novelapp

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

