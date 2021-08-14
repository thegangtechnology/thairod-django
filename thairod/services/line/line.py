import logging

from django.conf import settings
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage

from thairod.services.shippop.api import ShippopAPI

logger = logging.getLogger(__name__)


def send_line_message(line_uid: str, msg: str) -> bool:
    api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
    try:
        api.push_message(line_uid, TextSendMessage(text=msg))
        return True
    except LineBotApiError as e:
        logger.warning(e)
        return False


def send_line_tracking_message(line_uid: str, name: str, shippop_tracking_code: str):
    tracking_url = ShippopAPI().tracking_link(shippop_tracking_code)
    msg = settings.LINE_TRACKING_MESSAGE.format(name=name, tracking_url=tracking_url)
    return send_line_message(line_uid, msg)


def send_line_order_created_message(line_uid: str, name: str, order_id: int):
    msg = settings.LINE_ORDER_CREATED_MESSAGE.format(name=name,
                                                     order_id=order_id)
    return send_line_message(line_uid, msg)


def send_line_patient_address_confirmation_message(line_uid: str, patient_name: str,
                                                   patient_confirmation_url: str):
    msg = settings.LINE_PATIENT_CONFIRM_MESSAGE.format(name=patient_name,
                                                       patient_confirmation_url=patient_confirmation_url)
    return send_line_message(line_uid, msg)
