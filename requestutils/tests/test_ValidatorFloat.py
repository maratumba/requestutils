import nose.tools as nt
import validators


class TestValidatorFloat():

    @classmethod
    def setup_class(cls):
        cls.validator = validators.ValidatorFloat()

    def test_validates_int(self):
        nt.eq_(self.validator.check(1), 1)

    def test_validates_float(self):
        nt.eq_(self.validator.check(1.1), 1.1)

    def test_raises_on_invalid_string(self):
        invalid_input = 'test'
        nt.assert_raises(validators.ValidatorError, self.validator.check, invalid_input)
        try:
            self.validator.check(invalid_input)
        except validators.ValidatorError as e:
            nt.eq_(e.message, 'Supplied parameter <{}> is not a valid float value'.format(invalid_input))

    def test_description(self):
        nt.eq_(self.validator.description, 'Validate parameter if float value')
