import nose.tools as nt
import validators


class TestValidatorInt():

    @classmethod
    def setup_class(cls):
        cls.validator = validators.ValidatorInt()

    def test_validates_int(self):
        nt.eq_(self.validator.check(1), 1)

    def test_raises_on_invalid_string(self):
        invalid_input = 'test'
        nt.assert_raises(validators.ValidatorError, self.validator.check, invalid_input)
        try:
            self.validator.check(invalid_input)
        except validators.ValidatorError as e:
            nt.eq_(e.message, 'Supplied parameter <{}> is not a valid integer value'.format(invalid_input))

    def test_raises_on_float_input(self):
        invalid_input = '1.1'
        nt.assert_raises(validators.ValidatorError, self.validator.check, invalid_input)
        try:
            self.validator.check(invalid_input)
        except validators.ValidatorError as e:
            nt.eq_(e.message, 'Supplied parameter <{}> is not a valid integer value'.format(invalid_input))

    def test_description(self):
        nt.eq_(self.validator.description, 'Validate parameter if integer value')
