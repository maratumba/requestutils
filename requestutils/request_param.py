# -*- coding: utf-8 -*-
import validators


class RequestParam(object):

    def __init__(self, varname, name=None, required=True, default=None, unit=None, description=None, validators=[]):
        self.varname = varname          # Will use this to pull value from the query string
        self.name = name                # Human readable title
        self.unit = unit                # Measurment units ? m/s², m, deg ...
        self.value = None               # Once validated, the value of the parameter will be stored here
        self.required = required        # Will fail validation if required parameter with no default value is not found
        self.description = description  # A human readable description of this parameter
        self.validators = validators    # List of validators to run against this value
        self.default = default          # Default value of this parameter
        self.is_bound = False           # True when parameter is bound to a value from the request
        self.is_valid = False           # True once validation ran and found this parameter valid
        self.output_formatter = None

    def getValue(self):
        try:
            return self.output_formatter(self.value)
        except TypeError:
            return self.value

    def setOutputFormatter(self, callable):
        self.output_formatter = callable

    def addValidator(self, validator):
        '''
        Add a validator to this parameter
        '''
        self.validators.append(validator)

    def bind(self, handler):
        '''
        attach request parameter value to this parameter
        the value is looked up in the request parameters using the self.varname attribute
        '''
        try:
            self.value = handler.get_argument(self.varname)
        except:
            self.value = None
        self.is_bound = True

    def validate(self):
        '''
        run all validators on this parameter
        '''
        if len(self.validators) is 0:
            raise validators.ValidatorError(
                "Parameter {varname} can not be validated because it has no validators".format(**self.__dict__)
            )

        if self.required is True and self.value is None:
            if self.default is None:
                raise validators.ValidatorError("Required parameter {varname} is missing".format(**self.__dict__))
            else:
                self.value = self.default

        for validator in self.validators:
            self.value = validator.check(self.value)
        self.is_valid = True

    def addTo(self, request):
        request.addParam(self)
        return self

    def describe(self):
        return self.description
