# RPDB
A relational database using python and json

I don't know much about databases, so this may be better described as a relational interpreter.

## Brief example
This is explaied below in **Conceptual overview**
`mem_seg = newMemorySegment()`
<br>`person = Noun(mem_seg, "person").addr`
<br>`bob = Noun(mem_seg, "Bob", person).addr`
<br>`billy = Noun(mem_seg, "Billy", person).addr`
<br>`siblings = LinkingVerb(mem_seg, "is siblings").addr`
<br>`Link(mem_seg, bob, siblings, billy)`
<br>`write_mem_seg(mem_seg, "test.json")`
<br>`mem_seg = load_mem_seg("test.json")`

## Conceptual overview
The premise is that all systems can be described using objects and relations between those objects.
There are three classes I made to make such descriptions programmatically.
I have given them names from grammar because that was the easiest way for me to summarize it for myself.
<br>Each of these classes needs to be passed a MemorySegment object. 
MemorySegment is not designed specifically for this project, and there is a bit of extra setup needed, so use `newMemorySegment` to get a MemorySegment object to pass to new instances of the classes below.
<br>`mem_seg = newMemorySegment()`
<br> All instances of the below classes are referenced by their "address" (index) in the `MemorySegment`.
- **Noun** - This is the "thing" or "object." Every `Noun` has a `name`: `person = Noun(mem_seg, "person").addr`
<br>Each `Noun` can optionally be an `instance_of` another `Noun`: 
<br>`bob = Noun(mem_seg, "Bob", person).addr`
<br>`billy = Noun(mem_seg, "Billy", person).addr`
- **LinkingVerb** - These are words/phrases that are the types of relations, or "links", that can be made (eg "is a", "are", "owns", "was"). 
<br>`is_a = LinkingVerb(mem_seg, "is a").addr`
<br>'siblings = LinkingVerb(mem_seg, "is siblings").addr`
- **Link** - This is what relates `Nouns` to each other: `Link(mem_seg, bob, siblings, billy)` - read as "Bob is siblings with Billy"
<br>When a new `Noun` is initialized, if the `instance_of` parameter is not `None`, it creates a `Link` between itself and the `instance_of``Noun`: `Link(self.addr, is_a, self.instance_of)`
<br>It is possible to create a `Link` between any of these three classes, although I'm considering removing the ability to do so with `Link`s.

All instances of the above classes keep a list of the addresses of `Link`s they are involved in in their attribute `.links`.

## Class structure
- `Noun(mem, name, instance_of=None, addr=None, links=None)`
  - `.mem`
  - `.name`
  - `.instance_of`
  - `.addr`
  - `.links`
- `LinkingVerb(mem, name, addr=None, links=None)`
  - `.mem`
  - `.name`
  - `.addr`
  - `.links`
- `Link(mem, thing1, linking_verb, thing2, addr=None, links=None)`
  - `.mem`
  - `.thing1`
  - `.linking_verb`
  - `.thing2`
  - `.links`
- They all share:
  - `.__dict__()`
  - `.delete()` - use instead of `del <Noun/LinkingVerb/Link>`.
  - `.add_link(link_addr)` - adds `link_addr` to `self.links`. This is done automatically every time a new `Link` is created.
  - `.remove_link(link_addr)` - removes `link_addr` from `self.links`. Called by `Link.delete()`.
  - `.list_links()` - return list of `Link` objects in `self.links`.
  - `.list_linked()` - return list of objects involved in links in `self.links`.
