import json


class MemorySegment(list):
    """
    The idea is to have a modified list class for storing objects that care about their address.
    It provides ways of manipulating the list that avoid changing the locations where the object pointers are stored.
    """
    HOLE = object()
    def __init__(self, iterable: [object] = None, empty_values: [int] = None):
        """
        :param iterable: [object] If initializing with a populated list
        :param empty_values: [int] list of indices storing "None"
        """
        if empty_values is None:
            empty_values = []
        if iterable is None:
            iterable = []
        else:
            while True:
                try:
                    index = iterable.index(None)
                except ValueError:
                    break
                iterable[index] = self.HOLE

        super(MemorySegment, self).__init__(iterable)

        self.empty_values = empty_values

        if self:
            self.check_empty_values()

    def __delitem__(self, index):
        if hasattr(self[index], 'del'):
            self[index].__del__()
        self[index] = self.HOLE

    def __iter__(self):
        return (
            item
            for item in super().__iter__()
            if item is not None
        )

    def __getitem__(self, item):
        value = super().__getitem__(item)
        if value is self.HOLE:
            return self.HOLE
        else:
            return value

    def __setitem__(self, key, value):
        # print("Use del or .store_obj()")
        super().__setitem__(key, value)

    def __dict__(self):
        # TODO: currently only works if stored objects have .__dict__() defined
        dictified = {
            "__class__": self.__class__.__name__,
            "__module__": self.__module__,
            'empty_values': self.empty_values,
            'iterable': []
        }

        for item in self:
            if item is self.HOLE or item is None:
                dictified['iterable'].append(self.HOLE)
            elif hasattr(item, '__dict__'):
                dictified['iterable'].append(item.__dict__())
            else:
                dictified['iterable'].append(item)
        return dictified

    def store_obj(self, object_, addr=None):
        # TODO: decide if this if statement is helpful or not
        if addr is None:
            if hasattr(object_, "addr"):
                # print("storing object at object.addr")
                if object_.addr:
                    addr = object_.addr

        if addr is None:
            if len(self.empty_values) > 0:
                addr = self.empty_values[0]
                self[addr] = object_
                self.empty_values = self.empty_values[1:]
            else:
                self.append(object_)
                addr = len(self) - 1
        else:
            if len(self) <= addr:
                while len(self) < addr:
                    self.empty_values.append(len(self))
                    self.append(self.HOLE)
                self.append(object_)
            else:
                if self[addr] is self.HOLE:
                    self[addr] = object_
                else:
                    addr = -1
                    print("Unable to store object; index already occupied.")
        return addr

    def delete_obj(self, addr):
        del self[addr]

    def check_empty_values(self):
        for index in self.empty_values:
            if self[index] is not self.HOLE:
                self.empty_values = self.empty_values[:index] + self.empty_values[index+1:]

        for index in range(len(self)):
            if self[index] is self.HOLE:
                self.empty_values.append(index)

    def search(self, attr: str, value):
        results = []
        for index, item in enumerate(self):
            if hasattr(item, attr):
                if getattr(item, attr) == value:
                    results.append(index)
        return results
