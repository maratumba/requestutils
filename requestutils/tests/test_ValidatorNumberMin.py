import nose.tools as nt
import validators


class TestValidatorNumberMin():

    @classmethod
    def setup_class(cls):
        cls.validator = validators.ValidatorNumberMin(3)

    def test_passes_valid_int_input(self):
        assert self.validator.check(4)

    def test_passes_valid_float(self):
        assert self.validator.check(4.4)

    def test_passes_valid_float_from_string(self):
        assert self.validator.check('4.4')

    def test_fails_invalid_number(self):
        nt.assert_raises(validators.ValidatorError, self.validator.check, 'test')
        try:
            self.validator.check('test')
        except validators.ValidatorError as e:
            nt.eq_(e.message, 'Supplied parameter <test> is not a valid float value')

    def test_fails_too_small(self):
        nt.assert_raises(validators.ValidatorError, self.validator.check, 2)
        try:
            self.validator.check(2)
        except validators.ValidatorError as e:
            nt.eq_(e.message, 'Supplied parameter <2.0> is less than minimum value of 3')
            nt.eq_(e.errorlist, None)

    def test_description(self):
        nt.eq_(self.validator.description, 'Validate parameter if greater than minval 3')
