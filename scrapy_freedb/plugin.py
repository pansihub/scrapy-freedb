import json
import logging
from .base import SpiderPlugin, BooleanPluginParameter, StringPluginParameter
from scrapy.settings import Settings


logger = logging.getLogger(__name__)


class Plugin(SpiderPlugin):
    parameters = [
        BooleanPluginParameter('ENABLED', required=True, default_value=False),
        StringPluginParameter('freedb_token'),
        StringPluginParameter('freedb_baseurl'),
        StringPluginParameter('freedb_dbname'),
        StringPluginParameter('freedb_colname'),
    ]
    plugin_name = 'freedb_plugin'
    settings = None

    def perform(self, settings: Settings = None, plugin_settings: dict = None, **kwargs):
        if not get_bool(plugin_settings.get('ENABLED', 'false')):
            return

        logger.info('scrapy-freedb plugin enabled.')

        item_pipelines = settings.getdict('ITEM_PIPELINES')
        item_pipelines['scrapy_freedb.middleware.pipeline.FreedbSaveItemPipeline'] = 100
        settings.set('ITEM_PIPELINES', item_pipelines)
        settings.set('DUPEFILTER_CLASS', 'scrapy_freedb.middleware.dupefilter.FreedbDupefilter')
        # only write setting when exact value assigned. 
        # settings also can be populated through -s parameters.
        freedb_baseurl = plugin_settings.get('FREEDB_BASEURL')
        if freedb_baseurl:
            settings.set('FREEDB_BASEURL', freedb_baseurl)

        freedb_token = plugin_settings.get('FREEDB_TOKEN')
        if freedb_token:
            settings.set('FREEDB_TOKEN', freedb_token)

        freedb_dbname = plugin_settings.get('FREEDB_DBNAME')
        if freedb_dbname:
            settings.set('FREEDB_DBNAME', freedb_dbname)

        freedb_colname = plugin_settings.get('FREEDB_COLNAME')
        if freedb_colname:
            settings.set('FREEDB_COLNAME', freedb_colname)

        freedb_id_mapper = plugin_settings.get('FREEDB_ID_MAPPER')
        if freedb_id_mapper:
            settings.set('FREEDB_ID_MAPPER', freedb_id_mapper)

        freedb_id_field = plugin_settings.get('FREEDB_ID_FIELD')
        if freedb_id_field:
            settings.set('FREEDB_ID_FIELD', freedb_id_field)

    def apply(self, settings, **kwargs):
        plugin_settings = self.settings or {}
        self.perform(settings, plugin_settings)


def get_bool(value):
    try:
        return bool(int(value))
    except ValueError:
        if value in ("True", "true"):
            return True
        if value in ("False", "false"):
            return False
        raise ValueError("Supported values for boolean settings "
                         "are 0/1, True/False, '0'/'1', "
                         "'True'/'False' and 'true'/'false'")
