

class Klasa(object):

    def __init__(self):
        self.s = "k"



def fun(obiekt):

    obiekt.s = "dafasdf"


o = Klasa()
fun(o)
print(o.s)
