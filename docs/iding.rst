
IDing
=====

.. currentmodule:: suou.iding

...

SIQ
---

The main point of the SUOU library is to provide an implementation for the methods of SIS, a protocol for information exchange in phase of definition,
and of which SUOU is the reference implementation.

The key element is the ID format called SIQ, a 112-bit identifier format.

Here follow an extract from the `specification`_:

.. _specification: <https://yusur.moe/protocols/siq.html>

Why SIQ?
********

.. highlights::
   I needed unique, compact, decentralized, reproducible and sortable identifiers for my applications.
   
   Something I could reliably use as database key, as long as being fit for my purposes, in the context of a larger project, a federated protocol.

Why not ...
***********

.. highlights::
   * **Serial numbers**? They are relative. If they needed to be absolute, they would have to be issued by a single central authority for everyone else. Unacceptable for a decentralized protocol. 
   * **Username-domain identifiers**? Despite them being in use in other decentralized protocols (such as ActivityPub and Matrix), they are immutable and bound to a single domain. It means, the system sees different domains or usernames as different users. Users can't change their username after registration, therefore forcing them to carry an unpleasant or cringe handle for the rest of their life.
   * **UUID**'s? UUIDs are unreliable. Most services use UUIDv4's, which are just opaque sequences of random bytes, and definitely not optimal as database keys. Other versions exist (such as the timestamp-based [UUIDv7](https://uuidv7.org)), however they still miss something needed for cross-domain uniqueness. In any case, UUIDs need to waste some bits to specify their "protocol".
   * **Snowflake**s? Snowflakes would be a good choice, and are the inspiration for SIQ themselves. However, 64 bits are not enough for our use case, and Snowflake is *already making the necessary sacrifices* to ensure everything fits into 64 bits (i.e. the epoch got significantly moved forward).
   * **Content hashes**? They are based on content, therefore they require content to be immutable and undeletable. Also: collisions.
   * **PLC**'s (i.e. the ones in use at BlueSky)? [The implementation is cryptic](https://github.com/did-method-plc/did-method-plc). Moreover, it requires a central authority, and BlueSky is, as of now, holding the role of the sole authority. The resulting identifier as well is apparently random, therefore unorderable.
   * **ULID**'s? They are just UUIDv4's with a timestamp. Sortable? Yes. Predictable? No, random bits rely on the assumption of being generated on a single host — i.e. centralization. Think of them as yet another attempt to UUIDv7's.

Anatomy of a SIQ
****************


SIQ's are **112 bit** binary strings. Why 112? Why not 128? Idk, felt like it. Maybe to save space. Maybe because I could fit it into UUID some day — UUID already reserves some bits for the protocol.

Those 112 bits split up into:

* 56 bits of **timestamp**;
* 8 bits of process ("**shard**") information;
* 32 bits of **domain** hash;
* 16 bits of **serial** and **qualifier**.

Here is a graph of a typical SIQ layout:

```
0: tttttttt tttttttt tttttttt tttttttt tttttttt
40: uuuuuuuu uuuuuuuu ssssssss dddddddd dddddddd
80: dddddddd dddddddd nnnnnnnn nnqqqqqq

where:
t : timestamp -- seconds 
u : timestamp -- fraction seconds
s : shard
d : domain hash
n : progressive
q : qualifier (variable width, in fact)
```

Timestamp
*********

SIQ uses 56 bits for storing timestamp:

- **40 bits** for **seconds**;
- **16 bits** for **fraction seconds**.

There is no need to explain [why I need no less than 40 bits for seconds](https://en.wikipedia.org/wiki/Year_2038_problem).

Most standards — including Snowflake and ULID — store timestamp in *milliseconds*. It means the system needs to make a division by 1000 to retrieve second value.

But 1000 is almost 1024, right? So the last ten bits can safely be ignored and we easily obtain a UNIX timestamp by doing a right shi-&nbsp; wait.

It's more comfortable to assume that 1024 is nearly 1000. *Melius abundare quam deficere*. And injective mapping is there.

But rounding? Truncation? Here comes the purpose of the 6 additional trailing bits: precision control. Bits from dividing milliseconds o'clock are different from those from rounding microseconds.

Yes, most systems can't go beyond milliseconds for accuracy — standard Java is like that. But detecting platform accuracy is beyond my scope.

There are other factors to ensure uniqueness: *domain* and *shard* bits.

Domain, shard
*************

The temporal uniqueness is ensured by timestamp. However, in a distributed, federated system there is the chance for the same ID to get generated twice by two different subjects.

Therefore, *spacial* uniqueness must be enforced in some way.

Since SIQ's are going to be used the most in web applications, a way to differentiate *spacially* different applications is via the **domain name**.

I decided to reserve **32 bits** for the domain hash.

The algorithm of choice is **SHA-256** for its well-known diffusion and collision resistance. However, 256 bits are too much to fit into a SIQ! So, the last 4 bytes are taken.

*...*

Development and testing environments may safely set all the domain bits to 0.

Qualifiers
**********

The last 16 bits are special, in a way that makes those identifiers unique, and you can tell what is what just by looking at them.

Inspired by programming language implementations, such as OCaml and early JavaScript, a distinguishing bit affix differentiates among types of heterogeneous entities:

* terminal entities (leaves) end in ``1``. This includes content blobs, array elements, and relationships;
* non-leaves end in ``0``.

The full assigment scheme (managed by me) looks like this:

-------------------------------------------------------
Suffix       Usage      
=======================================================
``x00000``   user account 
``x10000``   application (e.g. API, client, bot, form) 
``x01000``   event, task 
``x11000``   product, subscription 
``x00100``   user group, membership, role 
``x10100``   collection, feed 
``x01100``   invite 
``x11100``   *unassigned* 
``x00010``   tag, category 
``x10010``   *unassigned* 
``x01010``   channel (guild, live chat, forum, wiki~) 
``x11010``   *unassigned* 
``xx0110``   thread, page 
``xx1110``   message, post, revision 
``xxx001``   3+ fk relationship 
``xxx101``   many-to-many, hash array element 
``xxx011``   array element (one to many) 
``xxx111``   content 
--------------------------------------------------------


The leftover bits are used as progressive serials, incremented as generation continues, and usually reset when timestamp is incremented.

Like with snowflakes and ULID's, if you happen to run out with serials, you need to wait till timestamp changes. Usually around 15 microseconds.

Storage
*******

It is advised to store in databases as *16 byte binary strings*.

-  In MySQL/MariaDB, it's ``VARBINARY(16)``.

The two extra bytes are to ease alignment, and possible expansion of timestamp range — even though it would not be an issue until some years after 10,000 CE.

It is possible to fit them into UUID's (specifically, UUIDv8's — custom ones), taking advantage from databases and libraries implementing a UUID type — e.g. PostgreSQL.

Unfortunately, nobody wants to deal with storing arbitrarily long integers — lots of issues pop up by going beyond 64. 128 bit integers are not natively supported in most places. Let alone 112 bit ones.

(end of extract)

Implementation
**************

.. autoclass:: Siq

.. autoclass:: SiqGen

.. automethod:: SiqGen.__init__
.. automethod:: SiqGen.generate

Snowflake
---------

SUOU also implements \[the Discord flavor of\] Snowflake ID's.

This flavor of Snowflake requires an epoch date, and consists of:
* 42 bits of timestamp, with millisecond precision;
* 10 bits for, respectively, worker ID (5 bits) and shard ID (5 bits);
* 12 bits incremented progressively.


.. autoclass:: suou.snowflake.Snowflake

.. autoclass:: suou.snowflake.SnowflakeGen


Other ID formats
----------------

Other ID formats (such as UUID's, ULID's) are implemented by other libraries.

In particular, Python itself has support for UUID in the Standard Library.


