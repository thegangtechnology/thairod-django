class PatientAlreadyConfirmedException(Exception):

    def __init__(self):
        self.message = 'Patient already confirmed. Cannot confirm again'


class OrderAlreadyConfirmedException(Exception):

    def __init__(self):
        self.message = 'Order already confirmed. Cannot make another order of the same request'


class HashExpired(Exception):
    pass
