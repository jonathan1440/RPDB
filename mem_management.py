import json


class MemorySegment(list):
    HOLE = object()

    def __init__(self, iterable=None, empty_values=None):
        if empty_values is None:
            empty_values = []
        if iterable is None:
            iterable = []

        super().__init__(iterable)

        self.empty_values = empty_values

    def __delitem__(self, index):
        if hasattr(self[index], 'del'):
            self[index].__del__()
        self[index] = self.HOLE

    def __iter__(self):
        return (
            item
            for item in super().__iter__()
            if item is not self.HOLE
        )

    def __getitem__(self, item):
        value = super().__getitem__(item)
        if value is self.HOLE:
            return None
        else:
            return value

    def __setitem__(self, key, value):
        # print("Use del or .store_obj()")
        super().__setitem__(key, value)

    def __dict__(self):
        dictified = {
            "__class__": self.__class__.__name__,
            "__module__": self.__module__,
            'empty_values': self.empty_values,
            'iterable': []
        }

        for item in self:
            if item is self.HOLE:
                continue
            elif hasattr(item, '__dict__'):
                dictified['iterable'].append(item.__dict__())
            else:
                dictified['iterable'].append(item)
        return dictified

    def store_obj(self, object_, addr=None):
        if addr is None:
            if hasattr(object_, "addr"):
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
                    self.append(None)
                self.append(object_)
            else:
                if self[addr] is None:
                    self[addr] = object_
                else:
                    addr = -1
                    print("Unable to store object; index already occupied.")
        return addr

    def delete_obj(self, addr):
        self[addr] = self.HOLE

    def check_empty_values(self):
        for index in self.empty_values:
            if self[index] is not None:
                self.empty_values = self.empty_values[:index] + self.empty_values[index+1:]

        for index, item in enumerate(self):
            if item is None:
                self.empty_values.append(index)

    def search(self, attr: str, value):
        results = []
        for index, item in enumerate(self):
            if hasattr(item, attr):
                if getattr(item, attr) == value:
                    results.append(index)
        return results


def write_segments(json_filepath: str, segments: [MemorySegment], segment_order: [str]):
    data = {}

    for index, segment in enumerate(segments):
        data[segment_order[index]] = segment.__dict__()

    with open(json_filepath, 'w') as file:
        file.truncate()
        json.dump(data, file)


def load_segments(json_filepath: str):
    with open(json_filepath, 'r') as file:
        return json.load(file)
