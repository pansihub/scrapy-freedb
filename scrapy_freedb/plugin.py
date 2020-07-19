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

    def validate(self, parameters):
        try:
            enabled = get_bool(parameters['ENABLED'])
        except (ValueError, KeyError):
            return False

        return True

    def execute(self, parameters):
        enabled = get_bool(parameters.get('ENABLED', True))
        ret_dict = []
        if enabled:
            ret_dict.extend([
                {
                    'op': 'set_dict',
                    'target': 'ITEM_PIPELINES',
                    'key': 'freedb_plugin.middleware.pipeline.FreedbSaveItemPipeline',
                    'value': 100,
                },
                {
                    'op': 'set_var',
                    'var': 'DUPEFILTER_CLASS',
                    'value': 'freedb_plugin.middleware.dupefilter.FreedbDupefilter'
                },
                {
                    'op': 'set_var',
                    'var': 'FREEDB_BASEURL',
                    'value': parameters.get('freedb_baseurl')
                },
                {
                    'op': 'set_var',
                    'var': 'FREEDB_TOKEN',
                    'value': parameters.get('freedb_token')
                },
                {
                    'op': 'set_var',
                    'var': 'FREEDB_DBNAME',
                    'value': parameters.get('freedb_dbname')
                },
                {
                    'op': 'set_var',
                    'var': 'FREEDB_COLNAME',
                    'value': parameters.get('freedb_colname')
                },
                {
                    'op': 'set_var',
                    'var': 'FREEDB_ID_MAPPER',
                    'value': parameters.get('freedb_id_mapper')
                }
            ])
        return ret_dict

    def perform(self, settings: Settings, plugin_settings):
        if not get_bool(plugin_settings.get('ENABLED', 'false')):
            return

        logger.info('scrapy-freedb plugin enabled.')

        item_pipelines = settings.getdict('ITEM_PIPELINES')
        item_pipelines['scrapy_freedb.middleware.pipeline.FreedbSaveItemPipeline'] = 100
        settings.set('ITEM_PIPELINES', item_pipelines)
        settings.set('DUPEFILTER_CLASS', 'scrapy_freedb.middleware.dupefilter.FreedbDupefilter')
        settings.set('FREEDB_BASEURL', plugin_settings.get('FREEDB_BASEURL'))
        settings.set('FREEDB_TOKEN', plugin_settings.get('FREEDB_TOKEN'))
        settings.set('FREEDB_DBNAME', plugin_settings.get('FREEDB_DBNAME'))
        settings.set('FREEDB_COLNAME', plugin_settings.get('FREEDB_COLNAME'))
        settings.set('FREEDB_ID_MAPPER', plugin_settings.get('FREEDB_ID_MAPPER'))


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


TEMPLATE = '''
try: SPIDER_MIDDLEWARES
except NameError: SPIDER_MIDDLEWARES = {}
SPIDER_MIDDLEWARES['scrapy_splitvariants.SplitVariantsMiddleware']= 100

SPLITVARIANTS_ENABLED = %(enabled)s
'''


def execute(settings):
    enabled = get_bool(settings.get('ENABLED', True))
    return TEMPLATE % {'enabled': enabled}
