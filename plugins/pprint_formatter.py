import logging
from pprint import pformat

logger = logging.getLogger(__name__)

class PPrintFormatter(logging.Formatter):
    def format(self, record):
        if isinstance(record.msg, dict) or isinstance(record.msg, list):
            record.msg = pformat(record.msg, indent=4)
        return super().format(record)
    
logger.info("PPrintFormatter 已經載入")