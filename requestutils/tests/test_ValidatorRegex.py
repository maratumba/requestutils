import nose.tools as nt
import validators


class TestValidatorRegex():

    @classmethod
    def setup_class(cls):
        cls.validator = validators.ValidatorRegex('^test\d{3}.*')

    def test_pass_expression(self):
        assert self.validator.check('test123dasdasda')

    def test_fail_expression(self):
        nt.assert_raises(validators.ValidatorError, self.validator.check, 'testiii123dasdasda')

    def test_description(self):
        nt.eq_(self.validator.description, 'Validate parameter if matching regular expression ^test\\d{3}.*')
