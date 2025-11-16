# SIS Unified Object Underarmor

Good morning, my brother! Welcome **SUOU** (**S**IS **U**nified **O**bject **U**nderarmor), the Python library which speeds up and makes it pleasing to develop API, database schemas and stuff in Python.

It provides utilities such as:
* SIQ ([specification](https://yusur.moe/protocols/siq.html) - [copy](https://suou.readthedocs.io/en/latest/iding.html))
* signing and generation of access tokens, on top of [ItsDangerous](https://github.com/pallets/itsdangerous) *not tested and not working*
* helpers for use in Flask, [SQLAlchemy](https://suou.readthedocs.io/en/latest/sqlalchemy.html), and other popular frameworks
* i forgor 💀

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

## Features

Read the [documentation](https://suou.readthedocs.io/).

## Support

Just a heads up: SUOU was made to support Sakuragasaki46 (me)'s own selfish, egoistic needs. Not certainly to provide a service to the public.

As a consequence, 'add this add that' stuff is best-effort.

Expect breaking changes, disruptive renames in bugfix releases, sudden deprecations, years of unmantainment, or sudden removal of SUOU from GH or pip.

Don't want to depend on my codebase for moral reasons (albeit unrelated)? It's fine. I did not ask you.

**DO NOT ASK TO MAKE SUOU SAFE FOR CHILDREN**. Enjoy having your fingers cut.

## License

Licensed under the [Apache License, Version 2.0](LICENSE), a non-copyleft free and open source license.

This is a hobby project, made available “AS IS”, with __no warranty__ express or implied.

I (sakuragasaki46) may NOT be held accountable for Your use of my code.

> It's pointless to file a lawsuit because you feel damaged, and it's only going to turn against you. What a waste of money you could have spent on a vacation or charity, or invested in stocks.

Happy hacking.

