# class PrivateUserException(Exception):
#     def __init__(self):
#         return
#
#
# class UserDeletedException(Exception):
#     def __init__(self):
#         return


class ServerErrorException(Exception):
    def __init__(self):
        return

class NotEnoughFavorites(Exception):
    def __init__(self, count):
        self.count = count
        return
