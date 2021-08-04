from order.models import Order

ItemVariationID = int
StockCount = int


class FulFillerService:
    def fulfil_orders(self):
        pass

    def attempt_fulfil(self, order: Order):
        pass
