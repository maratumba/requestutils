import nose.tools as nt
import validators


class TestValidatorOR():

    @classmethod
    def setup_class(cls):
        cls.validator = validators.ValidatorOR([validators.ValidatorEqual(1), validators.ValidatorEqual(5)])

    def test_description(self):
        nt.eq_(self.validator.description, 'Validate if ANY of the conditions are met')

    def test_fail(self):
        nt.assert_raises(validators.ValidatorError, self.validator.check, 2)
        try:
            self.validator.check(2)
        except validators.ValidatorError as e:
            nt.eq_(e.message, 'Supplied parameter <2> did not match any condition')
            nt.eq_(len(e.errorlist), 2)
            nt.eq_(e.flatten(),
                   ['Supplied parameter <2> did not match any condition',
                    'Supplied parameter <2> does not equal <1>',
                    'Supplied parameter <2> does not equal <5>']
                   )

    def test_pass1(self):
        nt.eq_(self.validator.check(5), 5)

    def test_should_pass(self):
        assert self.validator.check(1)
