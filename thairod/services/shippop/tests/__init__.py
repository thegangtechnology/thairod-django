from thairod.services.shippop.data import ParcelData, AddressData, OrderLineData, OrderData


def load_test_data():
    parcel = ParcelData(name='name', weight=1, width=2, length=3, height=4)
    from_address = AddressData(name="from testing", address="123/456 Testor Tower", district="บางรัก",
                               state="บางรัก", province="กรุงเทพมหานคร", postcode="10200", tel="0850035533")
    to_address = AddressData(name="to testing", address="1231123/456 Testor Tower", district="บางรัก",
                             state="บางรัก", province="กรุงเทพมหานคร", postcode="10200", tel="0850035533")

    order_lines = [OrderLineData(from_address=from_address, to_address=to_address, parcel=parcel)]

    order_data = OrderData(email="k.ronnakrit@thegang.tech", success_url="http://shippop.com/?success",
                           fail_url="http://shippop.com/?fail", data=order_lines)

    return {
        "order_data": order_data,
        "order_lines": order_lines,
        "to_address": to_address,
        "from_address": from_address,
        "parcel": parcel,
    }
