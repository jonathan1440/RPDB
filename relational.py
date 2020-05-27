from mem_management import *
import json


class Linkable:
    def __init__(self, mem: MemorySegment, addr: int = None, links: [int] = None):
        """
        :param mem: MemorySegment
        :param addr: int index in mem
        :param links: [int] array of links involving self.addr
        """
        if links is None:
            links = []

        self.mem = mem
        self.links = links
        self.addr = self.mem.store_obj(self, addr)

    def __dict__(self):
        return dict({
            "__class__": self.__class__.__name__,
            "__module__": self.__module__,
            "addr": self.addr,
            "links": self.links
        })

    def add_link(self, link_addr: int):
        """
        :param link_addr: int addr of link
        :return: bool success?
        """
        if link_addr not in self.links:
            self.links.append(link_addr)
            return True
        print("Link already made")
        return False

    def remove_link(self, link_addr: int):
        """
        :param link_addr: int addr of link
        :return: bool success?
        """
        if link_addr in self.links:
            self.mem[link_addr].delete()
            link_index = self.links.indexOf(link_addr)
            self.links = self.links[:link_index] + self.links[link_index + 1:]
            return True
        return False

    def list_links(self):
        """
        :return: [Link] array of Link objects
        """
        return [self.mem[x] for x in self.links]

    def list_linked(self):
        """
        :return: [] array of linked objects
        """
        linked = []
        for link in self.list_links():
            if link.thing1 != self.addr:
                link.append(self.mem[link.thing1])
            elif link.thing2 != self.addr:
                link.append(self.mem[link.thing2])
        return linked

    def delete(self):
        # TODO: test delete functionality
        for link in self.links:
            self.mem[link].delete(self.addr)
        self.mem.delete_obj(self.addr)


class Word(Linkable):
    def __init__(self, mem: MemorySegment, name: str, addr: int = None, links: [int] = None):
        """
        :param mem: MemorySegment
        :param name: str
        :param addr: int index in mem
        :param links: [int] array of links involving self.addr
        """
        if links is None:
            links = []

        super(Word, self).__init__(mem, addr, links)

        self.name = name

    def __dict__(self):
        d = super(Word, self).__dict__()
        d.update(
            {"name": self.name}
        )
        return d

    def delete(self):
        super(Word, self).delete()
        del self


class LinkingVerb(Word):
    def __init__(self, mem: MemorySegment, name: str, addr: int = None, links: [int] = None):
        """
        Eg. "is" or "has". Generally denoting posession or definition.
        A linking verb called "is" should always be stored at index 0 of self.mem.
        This is done automatically by newMemorySegment().
        :param mem: MemorySegment
        :param name: str
        :param addr: int index in mem
        :param links: [int] array of links involving self.addr
        """
        if links is None:
            links = []

        super(LinkingVerb, self).__init__(mem, name, addr, links)

        print("Created LinkingVerb: ", self.__dict__())


is_a = 0


class Link(Linkable):
    def __init__(self, mem: MemorySegment, thing1: int, linking_verb: int, thing2: int, addr: int = None, links: [int] = None):
        """
        An instance of a LinkingVerb.
        Read as  "<thing1> <linking_verb> <thing2>" like "John is a person".
        :param mem: MemorySegment
        :param thing1: int index in mem
        :param linking_verb: int index in mem
        :param thing2: int index in mem
        :param addr: int index in mem
        :param links: [int] array of links involving self.addr
        """
        if links is None:
            links = []

        super(Link, self).__init__(mem, addr, links)

        self.thing1 = thing1
        self.linking_verb = linking_verb
        self.thing2 = thing2

        if self.addr != -1:
            self.mem[self.thing1].add_link(self.addr)
            self.mem[self.linking_verb].add_link(self.addr)
            self.mem[self.thing2].add_link(self.addr)

            print("Created new Link: ", self.__dict__())

    def __dict__(self):
        d = super(Link, self).__dict__()
        d.update(
            {
                "thing1": self.thing1,
                "linking_verb": self.linking_verb,
                "thing2": self.thing2
            }
        )
        return d

    def delete(self, ref_obj_addr=None):
        if ref_obj_addr != self.thing1:
            self.mem[self.thing1].remove_link(self.addr)
        if ref_obj_addr != self.linking_verb:
            self.mem[self.linking_verb].remove_link(self.addr)
        if ref_obj_addr != self.thing2:
            self.mem[self.thing2].remove_link(self.addr)
        super(Link, self).delete()
        del self


class Noun(Word):
    def __init__(self, mem: MemorySegment, name: str, instance_of: int = None, addr: int = None, links: [int] = None):
        """
        The objects that (generally) get linked.
        A Noun can be an instance of another Noun or None
        :param mem: MemorySegment
        :param name: str
        :param instance_of: int index in mem
        :param addr: int index in mem
        :param links: [int] array of links involving self.addr
        """
        if links is None:
            links = []

        super(Noun, self).__init__(mem, name, addr, links)

        self.instance_of = instance_of

        if self.instance_of is not None:
            Link(self.mem, self.addr, is_a, self.instance_of)

        print("Created new Noun: ", self.__dict__())

    def __dict__(self):
        d = super(Noun, self).__dict__()
        d.update(
            {"instance_of": self.instance_of}
        )
        return d


def newMemorySegment():
    """
    This is the Correct way to initialize a new MemorySegment object.
    :return: MemorySegment("is_a")
    """
    db = MemorySegment()
    LinkingVerb(db, "is a", is_a)
    return db


def write_mem_seg(data: MemorySegment, json_filepath: str):
    """
    :param data: MemorySegment
    :param json_filepath: str
    :return: None
    """
    with open(json_filepath, 'w') as file:
        file.truncate()
        json.dump(data.__dict__(), file)


def load_mem_seg(json_filepath: str):
    """
    Assumes that memory segment stored in json file is functional.
    :param json_filepath: str
    :return: MemorySegment
    """
    with open(json_filepath, 'r') as file:
        data = json.load(file)

    db = MemorySegment()
    db.empty_values = data["empty_values"]

    for obj in data["iterable"]:
        module = __import__(obj.pop("__module__"))
        class_ = getattr(module, obj.pop("__class__"))
        new_obj = {"mem": db}
        new_obj.update(obj)
        new_obj["links"] = []
        class_(**new_obj)

    return db


def testrun(mem_seg):
    DB = mem_seg
    person = Noun(DB, "person").addr
    jz = Noun(DB, "Jonathan", person).addr
    bz = Noun(DB, "Benjamin", person).addr
    sibling = LinkingVerb(DB, "are siblings").addr
    Link(DB, jz, sibling, bz)
    write_mem_seg(DB, "test.json")
    AB = load_mem_seg("test.json")
    print("loaded data equals written data?", AB.__dict__() == DB.__dict__())
