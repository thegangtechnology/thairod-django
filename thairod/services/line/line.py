import logging

from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage

from thairod.services.shippop.api import ShippopAPI
from thairod.settings import LINE_CHANNEL_ACCESS_TOKEN, LINE_TRACKING_MESSAGE

logger = logging.getLogger(__name__)


def send_line_message(line_uid: str, msg: str) -> bool:
    api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    try:
        api.push_message(line_uid, TextSendMessage(text=msg))
        return True
    except LineBotApiError as e:
        logger.warning(e)
        return False


def send_line_tracking_message(line_uid: str, name: str, shippop_tracking_code: str):
    tracking_url = ShippopAPI().tracking_link(shippop_tracking_code)
    msg = LINE_TRACKING_MESSAGE.format(name=name, tracking_url=tracking_url)
    return send_line_message(line_uid, msg)
