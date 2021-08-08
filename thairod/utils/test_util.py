from decimal import Decimal
from unittest.mock import patch

import sqlparse
from django.db.models import QuerySet
from django.test import TestCase as TC
from linebot import LineBotApi
from rest_framework.test import APITestCase as ATC

from thairod.services.shippop.api import ShippopAPI
from thairod.services.shippop.data import OrderResponse, OrderLineResponse, OrderData
from thairod.utils.load_seed import load_seed
from user.models import User


def debug_query(qs: QuerySet) -> str:
    return sqlparse.format(str(qs.query), reindent=True)


def patch_line_bot_api(cls):
    line_patch = patch.object(LineBotApi, 'push_message', return_value=None)
    line_patch.__enter__()
    cls.addClassCleanup(line_patch.__exit__, None, None, None)


def fake_shippop_create_order(self, order_data: OrderData) -> OrderResponse:
    return OrderResponse(
        status=True,
        purchase_id=12345,
        total_price=Decimal(20),
        lines=[
            OrderLineResponse(status=True,
                              tracking_code='1234',
                              price=Decimal(20),
                              discount=Decimal(10),
                              from_address=od.from_address,
                              to_address=od.to_address,
                              courier_tracking_code='',
                              courier_code=od.courier_code,
                              parcel=od.parcel)
            for od in order_data.data
        ]
    )


def patch_shippop(cls):
    create_order = patch.object(ShippopAPI, 'create_order', new=fake_shippop_create_order)
    confirm_order = patch.object(ShippopAPI, 'confirm_order', return_value='True')
    create_order.__enter__()
    confirm_order.__enter__()
    cls.addClassCleanup(create_order.__exit__, None, None, None)
    cls.addClassCleanup(confirm_order.__exit__, None, None, None)


class TestCase(TC):
    patch_line = True
    patch_shippop = True
    with_seed = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if cls.patch_line:
            patch_line_bot_api(cls)
        if cls.patch_shippop:
            patch_shippop(cls)
        if cls.with_seed:
            load_seed()


class APITestCase(ATC):
    patch_line = True
    patch_shippop = True
    with_seed = True
    login = True

    def set_up_user(self, is_staff=True, is_superuser=False):
        password = User.objects.make_random_password()
        self.user = User.objects.create(username='forceauth',
                                        email='testpassuser@thegang.tech',
                                        password=password,
                                        is_staff=is_staff, is_superuser=is_superuser
                                        )
        self.client.force_authenticate(self.user)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if cls.patch_line:
            patch_line_bot_api(cls)
        if cls.patch_shippop:
            patch_shippop(cls)
        if cls.with_seed:
            load_seed()
