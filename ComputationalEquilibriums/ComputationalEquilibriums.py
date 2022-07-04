
class ReferenceDistribution():

    #Type = None
    #ReferenceValue = None
    #Distribution = None

    def __init__(self, _type="Binary", _reference=0.0, _dist=[0,0]):
        self.Type = _type
        self.ReferenceValue = _reference
        self.Distribution = _dist

    def update_reference(self, _val):
        self.ReferenceValue = _val

    def update_distribution(self, _val):
        if _val <= self.ReferenceValue:
            self.Distribution[0] += 1
        else:
            self.Distribution[1] += 1



