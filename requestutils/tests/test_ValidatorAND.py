import nose.tools as nt
import validators


class TestValidatorAND():

    @classmethod
    def setup_class(cls):
        cls.validator = validators.ValidatorAND([validators.ValidatorEqual(1), validators.ValidatorNumberMax(5)])

    def test_description(self):
        nt.eq_(self.validator.description, 'Validate if ALL of the conditions are met')

    def test_fail(self):
        nt.assert_raises(validators.ValidatorError, self.validator.check, 2)
        try:
            self.validator.check(2)
        except validators.ValidatorError as e:
            nt.eq_(e.message, 'Supplied parameter <2> does not equal <1>')

    def test_should_pass(self):
        assert self.validator.check(1)
