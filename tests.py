import os
import unittest
from functional.relational import *
from functional.mem_management import *


class msTestClass:
    def __init__(self, name):
        self.name = name

    def __dict__(self):
        return {
            'name': self.name,
        }

    def __del__(self):
        print("item deleted")
        del self


class TestMemorySegment(unittest.TestCase):
    def test_MemorySegment(self):
        ditch = msTestClass("")

        ms = MemorySegment()

        ms = MemorySegment([1, 2, ditch])
        self.assertEqual(ms[0], 1)
        self.assertEqual(ms[2], ditch)

        del ms[2]
        self.assertEqual(ms[2], MemorySegment.HOLE)

        del ms[1]
        self.assertEqual(ms[1], MemorySegment.HOLE)

        ms.check_empty_values()
        self.assertEqual(ms.empty_values, [1, 2])

        ms.store_obj(2)
        self.assertEqual(ms[1], 2)

        ms.delete_obj(0)
        self.assertEqual(ms[0], MemorySegment.HOLE)

        lst = [
            msTestClass("a"),
            MemorySegment.HOLE,
            msTestClass("c"),
            msTestClass("a")
        ]
        ms = MemorySegment(lst)

        self.assertEqual(ms.empty_values, [1])
        self.assertEqual(ms.search("name", "a"), [0, 3])
        self.assertEqual(ms.search("name", "d"), [])
        self.assertEqual(ms.search("asdf", "asdf"), [])

        # TODO: MemorySegment.__dict__ may only work if all stored items have .__dict__ defined


class TestStorageMethods(unittest.TestCase):
    def test_methods(self):
        counter = 0
        test_path = "test.json"
        while os.path.exists(test_path):
            test_path = 'test'+str(counter)+".json"
            counter += 1

        ms = MemorySegment()
        Noun(ms, "a")
        Noun(ms, "b")
        Noun(ms, "c")
        Noun(ms, "a")

        write_mem_seg(ms, test_path)
        ns = load_mem_seg(test_path)
        self.assertTrue(ms.__dict__() == ns.__dict__())

        os.remove(test_path)


class TestRelationalMethods(unittest.TestCase):
    # TODO: complete this... later
    pass
