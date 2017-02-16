import nose.tools as nt
import validators


class TestValidatorNumberRange():

    @classmethod
    def setup_class(cls):
        cls.validator = validators.ValidatorNumberRange(3, 9)

    def test_description(self):
        nt.eq_(self.validator.description, 'Validate number inside range range 3 - 9')

    def test_should_pass(self):
        assert self.validator.check(5)

    def test_fail(self):
        nt.assert_raises(validators.ValidatorError, self.validator.check, 2)
        try:
            self.validator.check(2)
        except validators.ValidatorError as e:
            nt.eq_(e.message, 'Supplied parameter <2.0> is less than minimum value of 3')

        try:
            self.validator.check(10)
        except validators.ValidatorError as e:
            nt.eq_(e.message, 'Supplied parameter <10.0> is greater than maximum value of 9')
