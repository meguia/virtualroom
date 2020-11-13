from .Validator import Validator

class NumberValidator(Validator):

    def __init__(self, minvalue=None, maxvalue=None, additional_msg=None, int_only = False):
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.msg = additional_msg
        self.int_only = int_only

    def validate(self, value):
        if self.int_only:
            if not isinstance(value, int):
                raise TypeError(f'{self.msg} Expected {value!r} to be an int')
        else:
            if not isinstance(value, (int, float)):
                raise TypeError(f'{self.msg} Expected {value!r} to be an int or float')
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(
                f'{self.msg} Expected {value!r} to be at least {self.minvalue!r}'
            )
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(
                f'{self.msg} Expected {value!r} to be no more than {self.maxvalue!r}'
            )
