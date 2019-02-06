class ClientUI(object):
    def query_package(self):
        user_input = input(('\033[1;33m'
                            'Type the package name for test: '
                            '\033[m'))
        user_input = user_input.strip()
        return user_input

