from .Validator import Validator

class StringValidator(Validator):

    def __init__(
                self, 
                minsize=None, 
                maxsize=None, 
                predicate=None, 
                additional_msg =None
                ):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate
        self.msg = additional_msg

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'{self.msg} Expected {value!r} to be an str')
        if self.minsize is not None and len(value) < self.minsize:
            raise ValueError(
                f'{self.msg} Expected {value!r} to be no smaller than {self.minsize!r}'
            )
        if self.maxsize is not None and len(value) > self.maxsize:
            raise ValueError(
                f'{self.msg} Expected {value!r} to be no bigger than {self.maxsize!r}'
            )
        if self.predicate is not None and not self.predicate(value):
            raise ValueError(
                f'{self.msg} Expected {self.predicate} to be true for {value!r}'
            )
