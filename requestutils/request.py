import validators


class RequestError(Exception):
    pass


class Request(object):

    def __init__(self, parameters=None):
        if parameters is None:
            self.parameters = []
        else:
            self.parameters = parameters
        self.errors = []
        self.global_errors = []
        self.is_bound = False
        self.post_validators = []
        self.param_bag = []

    def bind(self, param_bag):
        self.param_bag = param_bag
        self.is_valid = False
        for parameter in self.parameters:
            parameter.bind(self.param_bag)
        self.is_bound = True

    def validate(self):

        self.errors = []
        self.global_errors = []
        for parameter in self.parameters:
            try:
                parameter.validate()
            except validators.ValidatorError as e:
                self.errors.append((parameter, e))

        if len(self.errors) is 0:
            self.is_valid = True
        else:
            self.is_valid = False

        self.runPostValidators()

    def runPostValidators(self):
        for postvalidator in self.post_validators:
            try:
                postvalidator(self)
            except validators.ValidatorGlobalError as e:
                self.global_errors.append(e)
        if len(self.global_errors):
            self.is_valid = False

    def getArgs(self):
        if self.is_valid is False:
            return None
        return {param.varname: param.getValue() for param in self.parameters}

    def addParam(self, parameter):
        self.parameters.append(parameter)

    def addPostValidator(self, postvalidator):
        self.post_validators.append(postvalidator)

    def getParam(self, param_varname):
        '''
        get a request parameter by varname
        or raise RequestError
        '''
        for param in self.parameters:
            if param.varname == param_varname:
                return param

        raise RequestError('Tried to use undefined request parameter <{}>'.format(param_varname))

    def describe(self):
        pass
