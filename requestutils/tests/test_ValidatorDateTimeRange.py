import nose.tools as nt
import validators
import datetime


class TestValidatorDateRange(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_description(self):
        validator = validators.ValidatorDateTimeRange('2007-03-04T21:08:12.000', '2007-04-04T21:08:12.000')
        nt.eq_(validator.description, 'Validate parameter if ISO8601 Date time between <2007-03-04T21:08:12.000> and <2007-04-04T21:08:12.000>')

    def test_fail_outside_range(self):
        '''
        should fail if date is outside range
        '''
        validator = validators.ValidatorDateTimeRange('2007-03-04T21:08:12.000', '2007-04-04T21:08:12.000')
        nt.assert_raises(validators.ValidatorError, validator.check, '2007-05-04T21:08:12.000')
        try:
            validator.check('2007-05-04T21:08:12.000')
        except validators.ValidatorError as e:
            nt.eq_(e.message, 'Supplied parameter <2007-05-04T21:08:12.000> is not a valid ISO8601 Date time betwen <2007-03-04T21:08:12.000> and <2007-04-04T21:08:12.000>')


    def test_fail_outside_range_now(self):
        '''
        should fail if date is outside range
        '''
        now = datetime.datetime.now().isoformat()[:23]
        validator = validators.ValidatorDateTimeRange('2007-03-04T21:08:12.000', 'now')
        nt.assert_raises(validators.ValidatorError, validator.check, '2027-05-04T21:08:12.000')

        try:
            validator.check('2027-05-04T21:08:12.000')
        except validators.ValidatorError as e:
            nt.eq_(e.message, 'Supplied parameter <2027-05-04T21:08:12.000> is not a valid ISO8601 Date time betwen <2007-03-04T21:08:12.000> and <{}>'.format(now))

    def test_pass_inside_range_now(self):
        '''
        should pass when checking a parameter inside the range defined with now
        '''
        now = datetime.datetime.now().isoformat()[:23]
        validator = validators.ValidatorDateTimeRange('2007-03-04T21:08:12.000', 'now')
        nt.ok_(validator.check('2016-05-04T21:08:12.000'))

    def test_fail_invalid_param(self):
        '''
        should fail if cheching invalid date parameter
        '''
        validator = validators.ValidatorDateTimeRange('2007-03-04T21:08:12.000', '2007-04-04T21:08:12.000')
        nt.assert_raises(validators.ValidatorError, validator.check, '2007-i05-04T21:08:12.000')
        try:
            validator.check('2007-i05-04T21:08:12.000')
        except validators.ValidatorError as e:
            nt.eq_(e.message, 'Supplied parameter <2007-i05-04T21:08:12.000> is not a valid ISO8601 Date time')

    def test_create_daterange_now(self):
        '''
        should create a validator with current datetime as range
        '''
        now = datetime.datetime.now().isoformat()[:23]
        validator = validators.ValidatorDateTimeRange('2007-03-04T21:08:12.000')
        nt.eq_(validator.maxdt, now)
        nt.eq_(validator.description, 'Validate parameter if ISO8601 Date time between <2007-03-04T21:08:12.000> and <{}>'.format(now))
