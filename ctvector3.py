import pydicom

from pydicom.valuerep import DSfloat

class CTVector3:

    def __init__ (self, x = DSfloat("0"), y = DSfloat("0"), z = DSfloat("0")):
        self.x : DSfloat = x
        self.y : DSfloat = y
        self.z : DSfloat = z