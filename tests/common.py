from dataclasses import asdict


class TestDbReturnedRaw:
    def __init__(self, res):
        self._res = res

    def to_dict(self):
        return asdict(self._res)


class TestDbScalar:
    def __init__(self, res):
        self._res = res
        self._return = TestDbReturnedRaw

    def scalar(self):
        return self._return(res=self._res)
