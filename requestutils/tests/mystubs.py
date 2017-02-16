class StubQueryArgs(object):
    '''
    using this to mock the user request for my tests
    '''
    def __init__(self, args_dict):
        self.args_dict = args_dict

    def get_argument(self, argname):
        return self.args_dict[argname]

