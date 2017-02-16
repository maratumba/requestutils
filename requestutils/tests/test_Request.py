import nose.tools as nt
import request_param
import request
import validators


class StubRequestArgumentBag(object):

    def __init__(self, paramvals):
        self.params = paramvals

    def get_argument(self, name):
        return self.params[name]


class TestRequestParam():

    @classmethod
    def setup_class(cls):
        cls.rq_params = StubRequestArgumentBag({
            'latitude': 25,
            'longitude': 50
        })

    def test_pass(self):
        '''
        All params are ok. Should pass
        '''
        p1 = request_param.RequestParam('latitude',
                                        unit='lat degrees',
                                        description='event latitude',
                                        validators=[validators.ValidatorNumberRange(20, 30)])
        p2 = request_param.RequestParam('longitude',
                                        unit='longitude degrees',
                                        description='event longitude',
                                        validators=[validators.ValidatorNumberRange(40, 60)])

        rq = request.Request(parameters=[p1, p2])

        rq_params = StubRequestArgumentBag({
            'latitude': '25',
            'longitude': 50
        })
        rq.bind(rq_params)
        rq.validate()
        nt.eq_(rq.is_valid, True)

    def test_fail_on_invalid_params(self):
        '''
        Should fail on various errors
        '''
        p1 = request_param.RequestParam('latitude',
                                        unit='lat degrees',
                                        description='event latitude',
                                        validators=[validators.ValidatorNumberRange(20, 30)])
        p2 = request_param.RequestParam('longitude',
                                        unit='longitude degrees',
                                        description='event longitude',
                                        validators=[validators.ValidatorNumberRange(40, 60)])

        rq = request.Request(parameters=[p1, p2])

        rq_params = StubRequestArgumentBag({
            'latitude': 'w0',
            'longitude': 70
        })
        rq.bind(rq_params)
        rq.validate()
        nt.eq_(rq.is_valid, False)

        nt.eq_(rq.errors[0][1].message, 'Supplied parameter <w0> is not a valid float value')
        nt.eq_(rq.errors[1][1].message, 'Supplied parameter <70.0> is greater than maximum value of 60')

        rq_params = StubRequestArgumentBag({
            'latitude': 25,
            'longitude': 50
        })
        rq.bind(rq_params)
        rq.validate()
        nt.eq_(rq.is_valid, True)

        def pv1(request_object):
            '''
            silly validator raises if lat is smaller than lon
            '''
            lat = request_object.getParam('latitude')
            lon = request_object.getParam('longitude')
            if lat.value < lon.value:
                raise validators.ValidatorGlobalError('lat <{}> is smaller than lon <{}>'.format(lat.value, lon.value))

        rq.addPostValidator(pv1)
        rq.validate()
        nt.eq_(rq.is_valid, False)
        nt.eq_(rq.global_errors[0].message, 'lat <25.0> is smaller than lon <50.0>')
