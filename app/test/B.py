__author__ = 'fanghouguo'

# encoding = "utf-8"

from A import A


class B(A):

    def __init__(self):
        super(B, self).__init__()


b = B()

print
b
