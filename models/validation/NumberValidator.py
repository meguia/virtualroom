from .Validator import Validator

class NumberValidator(Validator):

    def __init__(self, minvalue=None, maxvalue=None, additional_msg=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.msg = additional_msg

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(additional_msg, f'Expected {value!r} to be an int or float')
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(
                f'{self.msg} Expected {value!r} to be at least {self.minvalue!r}'
            )
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(
                f'{self.msg} Expected {value!r} to be no more than {self.maxvalue!r}'
            )
