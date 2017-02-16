import nose.tools as nt
import validators
import request
from request_param import RequestParam
from mystubs import StubQueryArgs


class TestValidatorPostSmaller(object):

    def test_post_smaller_fail(self):
        '''
        fail if parameters are in the wrong order
        '''
        r = request.Request()
        RequestParam('minlat', validators=[validators.ValidatorFloat()]).addTo(r)
        RequestParam('maxlat', validators=[validators.ValidatorFloat()]).addTo(r)
        v1 = validators.ValidatorPostSmaller('minlat', 'maxlat')
        r.addPostValidator(v1)

        userparams = StubQueryArgs(dict(
            minlat=80,
            maxlat=60
        ))

        r.bind(userparams)
        r.validate()
        nt.eq_(r.global_errors[0].message, '<minlat> should be smaller than <maxlat>')

    def test_post_smaller_pass(self):
        '''
        pass if parameters are in the right order
        '''
        r = request.Request()
        RequestParam('minlat', validators=[validators.ValidatorFloat()]).addTo(r)
        RequestParam('maxlat', validators=[validators.ValidatorFloat()]).addTo(r)
        v1 = validators.ValidatorPostSmaller('minlat', 'maxlat')
        r.addPostValidator(v1)

        userparams = StubQueryArgs(dict(
            minlat=40,
            maxlat=60
        ))

        r.bind(userparams)
        r.validate()
        nt.eq_(r.global_errors, [])
