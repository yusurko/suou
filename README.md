# SIS Unified Object Underarmor

Good morning, my brother! Welcome the SUOU (SIS Unified Object Underarmor), a library for the management of the storage of objects into a database.

It provides utilities such as [SIQ](https://sakux.moe/protocols/siq.html), signing and generation of access tokens (on top of [ItsDangerous](https://github.com/pallets/itsdangerous)) and various utilities, including helpers for use in Flask and SQLAlchemy.

**It is not an ORM** nor a replacement of it; it works along existing ORMs (currently only SQLAlchemy is supported lol).

## Installation

**Python 3.10**+ with Pip is required.

```bash
$ pip install sakuragasaki46-suou
```

To install optional dependencies (i.e. `sqlalchemy`) for development use:

```bash
$ pip install sakuragasaki46-suou[sqlalchemy]
```

Please note that you probably already have those dependencies, if you just use the library.

## License

Licensed under the [Apache License, Version 2.0](LICENSE), a non-copyleft free and open source license.

This is a hobby project, made available “AS IS”, with __no warranty__ express or implied.

I (sakuragasaki46) may NOT be held accountable for Your use of my code.

> It's pointless to file a lawsuit because you feel damaged, and it's only going to turn against you. What a waste of money you could have spent on a vacation or charity, or invested in stocks.

