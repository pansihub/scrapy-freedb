import logging
from .freedb import FreedbClient


logger = logging.getLogger(__name__)


class FreedbSaveItemPipeline():
    def __init__(self, db_name, col_name, client: FreedbClient):
        self.db_name = db_name
        self.col_name = col_name
        self.client = client
    
    def process_item(self, item, spider):
        logger.debug('FreedbSaveItemPipeline process_item')
        self.client.save_document(self.db_name, self.col_name, dict(item))
        spider.logger.debug('FreedbSaveItemPipeline process_item done')
        return item

    @classmethod
    def from_crawler(cls, crawler):
        logger.info('FreedbSaveItemPipeline.from_crawler')
        settings = crawler.settings
        base_url = settings.get("FREEDB_BASEURL")
        token = settings.get('FREEDB_TOKEN')
        db_name = settings.get('FREEDB_DBNAME')
        col_name = settings.get('FREEDB_COLNAME')
        client = FreedbClient(base_url, token)
        return cls(db_name, col_name, client)
