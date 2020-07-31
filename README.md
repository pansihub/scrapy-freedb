# scrapy-freedb
A scrapy plugin support persist data on freedb and 
make incremental crawling.

It has a dupefilter wich interact to freedb to check 
there the document id is already existing.

To use this plugin directly in scrapy, add these 
settings in spider settings.py.

## Persist data

    ITEM_PIPELINES = {
        'scrapy_freedb.middleware.pipeline.FreedbSaveItemPipeline': 300,
    }

    FREEDB_BASEURL = 'http://localhost:8000'
    FREEDB_TOKEN = 'your_token_of_freedb'
    FREEDB_DBNAME = 'your_db'
    FREEDB_COLNAME = 'your_collection_name'

    # optional id field, if 'id' field is not in item, the pipeline will 
    # populate `id` field from this field before saving. The default value
    # of this is null, then no `id` value will be auto-populated.
    FREEDB_ID_FIELD = 'your_id_field'
    

Each spider will be mapped to a freedb db/collection.

Any item will be persist to JSON first, then post to freedb. 

## Incremental crawling

Set up the dupfilter class, on each request enqueuing, it will guess id with `FREEDB_ID_MAPPER`, and check whether there is doc on freedb collection with the same id.
The default FREEDB_ID_MAPPER will just return None whatever the request is.

    DUPEFILTER_CLASS = 'scrapy_freedb.middleware.dupefilter.FreedbDupefilter'

    FREEDB_ID_MAPPER = "package.some_module:some_func"

An example of id mapper can be a sha256 hash of request url.

    import hashlib

    def compute_hash_id(request):
        url = request.url
        hash = hashlib.sha256()
        hash.update(url.encode())
        return hash.hexdigest()

## pansi plugin spider.json

    {
        "plugins":[
            "scrapy-freedb"
        ]
        "plugin_settings":{
            "scrapy-freedb":{
                "ENABLED": true,
                "FREEDB_BASEURL":"",
                "FREEDB_TOKEN":"",
                "FREEDB_DBNAME":"",
                "FREEDB_COLNAME":"",
                "FREEDB_ID_MAPPER:""
            }
        }
    }