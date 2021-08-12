from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import List, Optional

from order.models import Order
from order_flow.models import OrderFlow
from thairod.utils.auto_serialize import AutoSerialize


def sensor_cid(cid: Optional[str]):
    if cid:
        return cid[-5:]
    else:
        return None


@dataclass
class OrderFlowSnapshotInfo(AutoSerialize):
    cid: str
    created: datetime.datetime
    order_created: bool

    @classmethod
    def from_order_flow(cls, order_flow: OrderFlow) -> OrderFlowSnapshotInfo:
        return OrderFlowSnapshotInfo(
            created=order_flow.doctor_link_hash_timestamp,
            cid=sensor_cid(order_flow.doctor_info.get('patient', {'cid': None}).get('cid', None)),
            order_created=order_flow.order_created
        )


@dataclass
class OrderSnapshotInfo(AutoSerialize):
    cid: str
    created: datetime.datetime

    @classmethod
    def from_order(cls, order: Order) -> OrderSnapshotInfo:
        return OrderSnapshotInfo(
            cid=sensor_cid(order.cid),
            created=order.order_time
        )


@dataclass
class QuickSnapshotResponse(AutoSerialize):
    order_flows: List[OrderFlowSnapshotInfo]
    orders: List[OrderSnapshotInfo]


class QuickSnapshotService(AutoSerialize):
    @classmethod
    def build_quick_snapshot_response(cls) -> QuickSnapshotResponse:
        return QuickSnapshotResponse(
            order_flows=[OrderFlowSnapshotInfo.from_order_flow(of)
                         for of in OrderFlow.objects.order_by('-doctor_link_hash_timestamp')[:10]],
            orders=[OrderSnapshotInfo.from_order(order)
                    for order in Order.objects.order_by('-order_time')[:10]]
        )
