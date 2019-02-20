class ClientUI(object):
    def query_args(self, arg):
        user_input = input(('\033[1;33m'
                            'Type the {0} for test: '
                            '\033[m').format(arg))
        user_input = user_input.strip()
        return user_input

