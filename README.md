# scrapy-freedb

This is a scrapy plugin support persisting data on freedb and/or 
archieving incremental crawling.

## Intruduction

It has a dupefilter wich interact to freedb to check 
there the document id is already existing.

To use this plugin directly in scrapy, add these 
settings in spider settings.py.

## Persist data

spider settings:

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

### Better solution of incremental crwaling

Since a dupelicate (against to the existing record) request filtering is on a Request object, 
and item persistent is on an Item object.
There may be no direct mapping between these two objects, and providing a consistant id mapper
function for the two types cause it too complicated. 

A good practice for this is to ignore the `id_mapper` settings at all. Each time you want to 
retrieve a potential item from a request, create such an Item instance, attach it to the 
`item` field of requests meta object (`request.meta['item']`), make sure you have configured
apropriate `id_field` settings and assigned correct value for this concrete request. Because
you have to provide an `id` before actually fetch the page, it is certainly you have to 
pick an `id` field from the information before the page, i.e. guess a thread id from the known
url, or just use the `url` of request is an option.




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