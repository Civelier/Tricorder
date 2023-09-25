import settings
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

class BaseSettings(settings.CommonSettings):
    def __init__(self):
        super().__init__("Base")
        options = {DEBUG : 'debug',
                   INFO : 'info',
                   WARNING : 'warning',
                   ERROR : 'error',
                   CRITICAL : 'critical'}
        BaseSettings.debugLevel = self.create_combo_property('base.debugLevel', 'Info', options)