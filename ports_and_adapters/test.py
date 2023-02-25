

class A:

    def __init__(self) -> None:
        print('Hi there')


def func(param):
    match param:
        case A():
            print('11')
        case _:
            print('22')


func(A())