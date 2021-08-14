from decimal import Decimal
from typing import Optional
from unittest.mock import patch, MagicMock

import sqlparse
from celery.contrib.testing.worker import start_worker
from django.db.models import QuerySet
from django.test import TestCase as TC
from django.test import override_settings
from django.test.runner import DiscoverRunner
from linebot import LineBotApi
from rest_framework.test import APITestCase as ATC

from thairod.celery import app
from thairod.services.shippop.api import ShippopAPI
from thairod.services.shippop.data import OrderResponse, OrderLineResponse, OrderData
from thairod.utils.load_seed import load_seed
from user.models import User


def debug_query(qs: QuerySet) -> str:
    return sqlparse.format(str(qs.query), reindent=True)


def patch_line_bot_api(cls):
    line_patch = patch.object(LineBotApi, 'push_message', return_value=None)
    mock = line_patch.__enter__()
    cls.addClassCleanup(line_patch.__exit__, None, None, None)
    return mock


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


def setup_celery_worker(cls):
    worker = start_worker(app, perform_ping_check=False)
    worker.__enter__()
    cls.addClassCleanup(lambda: worker.__exit__(None, None, None))


def setup_eager_celery(cls):
    ovs = override_settings(CELERY_TASK_ALWAYS_EAGER=True,
                            CELERGY_TASK_EAGER_PROPAGATES=True)
    ovs.__enter__()
    cls.addClassCleanup(lambda: ovs.__exit__(None, None, None))


def pre_setup(cls):
    if cls.with_bg_worker:
        setup_celery_worker(cls)
    else:
        setup_eager_celery(cls)


def post_setup(cls):
    if cls.patch_line:
        cls.line_mock = patch_line_bot_api(cls)
    if cls.patch_shippop:
        patch_shippop(cls)
    if cls.with_seed:
        load_seed()


class TestCase(TC):
    patch_line = True
    patch_shippop = True
    with_seed = True
    line_mock: Optional[MagicMock] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        post_setup(cls)

    def _pre_setup(self):
        super()._pre_setup()
        if self.line_mock is not None:
            self.line_mock.reset()


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
        post_setup(cls)


class ThairodTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        self.ovs = override_settings(CELERY_BROKER_URL='memory://localhost',
                                     CELERY_RESULT_BACKEND='rpc')
        self.ovs.__enter__()
        self.worker = start_worker(app, perform_ping_check=False)
        self.worker.__enter__()
        return super().setup_databases(**kwargs)

    def teardown_databases(self, old_config, **kwargs):
        super().teardown_databases(old_config, **kwargs)
        self.worker.__exit__(None, None, None)
        self.ovs.__exit__(None, None, None)
