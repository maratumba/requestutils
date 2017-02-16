import nose.tools as nt
import validators


class TestValidatorEqual():

    @classmethod
    def setup_class(cls):
        cls.validator = validators.ValidatorEqual('test')

    def test_passes_valid_int_input(self):
        nt.eq_(self.validator.check('test'), 'test')

    def test_fails_non_equal(self):
        nt.assert_raises(validators.ValidatorError, self.validator.check, 'not test')
        try:
            self.validator.check('not test')
        except validators.ValidatorError as e:
            nt.eq_(e.message, 'Supplied parameter <not test> does not equal <test>')

    def test_description(self):
        nt.eq_(self.validator.description, 'Validate parameter if equal to <test>')
