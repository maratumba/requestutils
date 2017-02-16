import nose.tools as nt
import validators
import datetime


class TestValidatorDateTime(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_description(self):
        validator = validators.ValidatorDateTime()
        nt.eq_(validator.description, 'Validate parameter if ISO8601 Date time')

    def test_return_datetime(self):
        validator = validators.ValidatorDateTime()
        dt = validator.check('2007-03-04T21:08:12.000')
        assert isinstance(dt, datetime.datetime)

    def test_fail_invalid_string(self):
        validator = validators.ValidatorDateTime()
        nt.assert_raises(validators.ValidatorError, validator.check, '2007-i03-04T21:08:12.000')
