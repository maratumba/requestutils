import re
import datetime


class ValidatorError(Exception):
    def __init__(self, message, errorlist=None):
        super(ValidatorError, self).__init__(message)
        self.errorlist = errorlist

    def flatten(self):
        output = []
        output.append(self.message)
        try:
            for (validator, exc) in self.errorlist:
                output += exc.flatten()
        except TypeError:
            pass
        return output


class ValidatorGlobalError(Exception):
    pass


class ValidatorBase(object):

    def formatError(self, param, error=None):
        if error is None:
            error = self.error
        return error.format(param=param, **self.__dict__)

    def getException(self, param, error=None, errorlist=None):
        return ValidatorError(self.formatError(param, error), errorlist=errorlist)

    def describe(self):
        return self.description


class ValidatorPostSmaller(object):
    '''
    validates if smaller is smaller than bigger
    '''

    def __init__(self, smaller, bigger,
                 allow_equal=False,
                 error="<{smaller}> should be smaller than <{bigger}>",
                 description="Ensure <{smaller}> is smaller than <{bigger}>"
                 ):
        self.smaller = smaller
        self.bigger = bigger
        self.allow_equal = allow_equal
        self.description = description.format(**self.__dict__)
        self.error = error

    def __call__(self, request):
        return self.check(request)

    def check(self, request):
        smallerp = request.getParam(self.smaller)
        biggerp = request.getParam(self.bigger)

        if not (smallerp.is_valid and biggerp.is_valid):
            raise ValidatorGlobalError(self.error.format(**self.__dict__))

        if (self.allow_equal is True) and (smallerp.value == biggerp.value):
            return

        if(biggerp.value <= smallerp.value):
            raise ValidatorGlobalError(self.error.format(**self.__dict__))


class ValidatorInt(ValidatorBase):

    def __init__(self,
                 description="Validate parameter if integer value",
                 error="Supplied parameter <{param}> is not a valid integer value"
                 ):

        self.description = description
        self.error = error

    def check(self, param):
        try:
            param = float(param)
        except ValueError:
            raise self.getException(param)
        if param.is_integer() is False:
            raise self.getException(param)
        return int(param)


class ValidatorFloat(ValidatorBase):

    def __init__(self,
                 description="Validate parameter if float value",
                 error="Supplied parameter <{param}> is not a valid float value"
                 ):

        self.description = description
        self.error = error

    def check(self, param):
        try:
            param = float(param)
        except ValueError:
            raise self.getException(param)
        return param


class ValidatorNumberMin(ValidatorBase):

    def __init__(self,
                 minval,
                 description="Validate parameter if greater than minval {minval}",
                 error="Supplied parameter <{param}> is less than minimum value of {minval}"
                 ):

        self.minval = minval
        self.description = description.format(**self.__dict__)
        self.error = error

    def check(self, param):
        param = ValidatorFloat().check(param)
        if param < self.minval:
            raise self.getException(param)
        return param


class ValidatorNumberMax(ValidatorBase):

    def __init__(self,
                 maxval,
                 description="Validate parameter if less than maxval {maxval}",
                 error="Supplied parameter <{param}> is greater than maximum value of {maxval}"
                 ):

        self.maxval = maxval
        self.description = description.format(**self.__dict__)
        self.error = error

    def check(self, param):
        param = ValidatorFloat().check(param)
        if param > self.maxval:
            raise self.getException(param)
        return param


class ValidatorRegex(ValidatorBase):

    def __init__(self,
                 regex,
                 description="Validate parameter if matching regular expression {regex}",
                 error="Supplied parameter <{param}> does not match regular expression {regex}"
                 ):
        self.regex = regex
        self.recompiled = re.compile(self.regex)
        self.description = description.format(**self.__dict__)
        self.error = error

    def check(self, param):
        if self.recompiled.match(param) is None:
            raise self.getException(param)
        return param


class ValidatorOR(ValidatorBase):

    def __init__(self,
                 validators,
                 description="Validate if ANY of the conditions are met",
                 error="Supplied parameter <{param}> did not match any condition"
                 ):
        self.validators = validators
        self.description = description
        self.error = error

    def check(self, param):
        errors = []
        for validator in self.validators:
            try:
                return validator.check(param)
            except ValidatorError as e:
                errors.append((validator, e))

        # if we reach this point then no validator matched
        raise self.getException(param, errorlist=errors)


class ValidatorAND(ValidatorBase):

    def __init__(self,
                 validators,
                 description="Validate if ALL of the conditions are met",
                 error="Supplied parameter <{param}> did not match all conditions"
                 ):
        self.validators = validators
        self.description = description.format(self.__dict__)
        self.error = error

    def check(self, param):
        for validator in self.validators:
            param = validator.check(param)

        return param


class ValidatorNumberRange(ValidatorAND):
    def __init__(self,
                 minval, maxval,
                 description="Validate number inside range range {minval} - {maxval}",
                 error="Supplied parameter <{param}> is not a valid number within range {minval} - {maxval}"
                 ):
        self.minval = minval
        self.maxval = maxval
        self.description = description.format(**self.__dict__)
        self.error = error
        self.validators = [
            ValidatorNumberMin(minval),
            ValidatorNumberMax(maxval)
        ]


class ValidatorEqual(ValidatorBase):
    def __init__(self,
                 equals,
                 description="Validate parameter if equal to <{equals}>",
                 error="Supplied parameter <{param}> does not equal <{equals}>"
                 ):
        self.equals = equals
        self.description = description.format(**self.__dict__)
        self.error = error

    def check(self, param):
        if param == self.equals:
            return param

        raise self.getException(param)


class ValidatorDateTime(ValidatorBase):

    def __init__(self,
                 description="Validate parameter if ISO8601 Date time",
                 error="Supplied parameter <{param}> is not a valid ISO8601 Date time"
                 ):
        self.description = description
        self.error = error

    def check(self, param):
        try:
            dt = datetime.datetime.strptime(param, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            raise self.getException(param)
        return dt


class ValidatorDateTimeMin(ValidatorBase):

    def __init__(self,
                 mindt,
                 description="Validate parameter if ISO8601 Date time later than <{mindt}>",
                 error="Supplied parameter <{param}> is not a valid ISO8601 Date time after <{mindt}>"
                 ):
        self.mindt = mindt
        self.validator_dt = ValidatorDateTime()
        self.mindt_obj = self.validator_dt.check(mindt)
        self.description = description.format(**self.__dict__)
        self.error = error

    def check(self, param):
        dt = self.validator_dt.check(param)
        if(dt < self.mindt_obj):
            raise self.getException(param)
        return dt


class ValidatorDateTimeMax(ValidatorBase):

    def __init__(self,
                 maxdt,
                 description="Validate parameter if ISO8601 Date time earlier than <{maxdt}>",
                 error="Supplied parameter <{param}> is not a valid ISO8601 Date time before <{maxdt}>"
                 ):
        self.maxdt = maxdt
        self.validator_dt = ValidatorDateTime()
        self.maxdt_obj = self.validator_dt.check(maxdt)
        self.description = description.format(**self.__dict__)
        self.error = error

    def check(self, param):
        dt = self.validator_dt.check(param)
        if(dt > self.maxdt_obj):
            raise self.getException(param)
        return dt


class ValidatorDateTimeRange(ValidatorBase):

    def __init__(self,
                 mindt, maxdt=None,
                 description="Validate parameter if ISO8601 Date time between <{mindt}> and <{maxdt}>",
                 error="Supplied parameter <{param}> is not a valid ISO8601 Date time betwen <{mindt}> and <{maxdt}>"
                 ):
        self.mindt = mindt

        if maxdt in (None, 'now', 'Now', 'NOW'):
            self.maxdt = datetime.datetime.now().isoformat()[:23]
        else:
            self.maxdt = maxdt

        self.validator_dt = ValidatorDateTime()
        self.mindt_obj = self.validator_dt.check(self.mindt)
        self.maxdt_obj = self.validator_dt.check(self.maxdt)
        if self.mindt_obj >= self.maxdt_obj:
            raise Exception('DateTimeRangeValidator initialized with bad data mindt: {mindt} and maxdt: {maxdt}'.format(self.__dict__))

        self.description = description.format(**self.__dict__)
        self.error = error

    def check(self, param):
        dt = self.validator_dt.check(param)
        if self.mindt_obj <= dt <= self.maxdt_obj:
            return dt

        raise self.getException(param)
