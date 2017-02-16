import nose.tools as nt
import request_param
import validators


class StubRequestArgumentBag(object):

    def __init__(self, paramvals):
        self.params = paramvals

    def get_argument(self, name):
        return self.params[name]


class TestRequestParam():

    @classmethod
    def setup_class(cls):
        pass

    def test_fail1(self):
        '''
        should raise KeyError if param tries to bind to request and request is missing that value
        '''
        request_params = StubRequestArgumentBag({
            'latitudes': 130
        })

        rp = request_param.RequestParam('latitude',
                                        unit='latutude degrees',
                                        description='Event latitude',
                                        validators=[validators.ValidatorNumberRange(20, 30)])

        nt.assert_raises(KeyError, rp.bind, request_params)

    def test_fail_validation(self):
        '''
        should fail if parameter value fails validation
        '''
        request_params = StubRequestArgumentBag({
            'latitude': 130
        })

        rp = request_param.RequestParam('latitude',
                                        unit='latutude degrees',
                                        description='Event latitude',
                                        validators=[validators.ValidatorNumberRange(20, 30)])
        rp.bind(request_params)
        nt.assert_raises(validators.ValidatorError, rp.validate)

        try:
            rp.validate()
        except validators.ValidatorError as e:
            nt.eq_(e.message, 'Supplied parameter <130.0> is greater than maximum value of 30')
