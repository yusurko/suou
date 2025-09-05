# Changelog

## 0.6.0

+ `.sqlalchemy` has been made a subpackage and split; `sqlalchemy_async` has been deprecated. Update your imports.
+ Add several new utilities to `.sqlalchemy`: `BitSelector`, `secret_column`, `a_relationship`, `SessionWrapper`, 
  `wrap=` argument to SQLAlchemy. Also removed dead batteries.
+ Add `.waiter` module. For now, non-functional.
+ Add `ArgConfigSource` to `.configparse`
+ Add more strings to `.legal` module

## 0.5.3

- Added docstring to `SQLAlchemy()`.
- More type fixes.

## 0.5.2

- Fixed poorly handled merge conflict leaving `.sqlalchemy` modulem unusable

## 0.5.1

- Fixed return types for `.sqlalchemy` module

## 0.5.0

+ `sqlalchemy`: add `unbound_fk()`, `bound_fk()`
+ Add `sqlalchemy_async` module with `SQLAlchemy()` async database binding. 
    * Supports being used as an async context manager
    * Automatically handles commit and rollback
+ `sqlalchemy_async` also offers `async_query()`
+ Changed `sqlalchemy.parent_children()` to use `lazy='selectin'` by default
+ Add `timed_cache()`, `alru_cache()`, `TimedDict()`, `none_pass()`, `twocolon_list()`, `quote_css_string()`, `must_be()`
+ Add module `calendar` with `want_*` date type conversion utilities and `age_and_days()`
+ Move obsolete stuff to `obsolete` package (includes configparse 0.3 as of now)
+ Add `redact` module with `redact_url_password()`
+ Add more exceptions: `NotFoundError()`, `BabelTowerError()`
+ Add `sass` module
+ Add `quart` module with `negotiate()`, `add_rest()`, `add_i18n()`, `WantsContentType`
+ Add `dei` module: it implements a compact and standardized representation for pronouns, inspired by the one in use at PronounDB

## 0.4.1

- Fixed return types for `.sqlalchemy` module.
- `sqlalchemy.parent_children()` now takes a `lazy` parameter. Backported from 0.5.1.

## 0.4.0

+ `pydantic` is now a hard dependency
+ `ConfigProperty` has now been generalized: check out `classtools.ValueProperty`
+ **BREAKING**: Changed the behavior of `makelist()`: **different behavior when used with callables**.
    * When applied as a decorator on callable, it converts its return type to a list.
    * Pass `wrap=False` to treat callables as simple objects, restoring the 0.3 behavior.
+ New module `lex` to make tokenization more affordable — with functions `symbol_table()` and `lex()`
+ Add `dorks` module and `flask.harden()`. `dorks` contains common endpoints which may be target by hackers
+ Add `sqlalchemy.bool_column()`: make making flags painless
+ Introduce `rb64encode()` and `rb64decode()` to deal with issues about Base64 and padding
    * `b64encode()` and `b64decode()` pad to the right
    * `rb64encode()` and `rb64decode()` pad to the left, then strip leading `'A'` in output 
+ Added `addattr()`, `PrefixIdentifier()`, `mod_floor()`, `mod_ceil()`
+ First version to have unit tests! (Coverage is not yet complete)

## 0.3.8

- Fixed return types for `.sqlalchemy` module.
- `sqlalchemy.parent_children()` now takes a `lazy` parameter. Backported from 0.5.1.

## 0.3.7

- Fixed a bug in `b64decode()` padding handling which made the function inconsistent and non injective. Now, leading `'A'` is NEVER stripped.

## 0.3.6

- Fixed `ConfigValue` behavior with multiple sources. It used to iterate through all the sources, possibly overwriting; now, iteration stops at first non-missing value

## 0.3.5

- Fixed cb32 handling. Now leading zeros in SIQ's are stripped, and `.from_cb32()` was implemented

## 0.3.4

- Bug fixes in `.flask_restx` regarding error handling
- Fixed a bug in `.configparse` dealing with unset values from multiple sources

## 0.3.3

- Fixed leftovers in `snowflake` module from unchecked code copying — i.e. `SnowflakeGen.generate_one()` used to require an unused typ= parameter
- Fixed a bug in `id_column()` that made it fail to provide a working generator — again, this won't be backported

## 0.3.2

- Fixed bugs in Snowflake generation and serialization of negative values

## 0.3.0

- Fixed `cb32encode()` and `b32lencode()` doing wrong padding — **UNSOLVED in 0.2.x** which is out of support, effective immediately
- **Changed behavior** of `kwargs_prefix()` which now removes keys from original mapping by default
- Add SQLAlchemy auth loaders i.e. `sqlalchemy.require_auth_base()`, `flask_sqlalchemy`.
  What auth loaders do is loading user token and signature into app
- `sqlalchemy`: add `parent_children()` and `create_session()`
- Implement `UserSigner()`
- Improve JSON handling in `flask_restx`
- Add base2048 (i.e. [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)) codec
- Add `split_bits()`, `join_bits()`, `ltuple()`, `rtuple()`, `ssv_list()`, `additem()`
- Add `markdown` extensions
- Add Snowflake manipulation utilities

## 0.2.3

- Bug fixes in `classtools` and `sqlalchemy`

## 0.2.1

- Add `codecs.jsonencode`

## 0.2.0

- Add `i18n`, `itertools`
- Add `toml` as a hard dependency
- Add support for Python dicts as `ConfigSource`
- Implement ULID -> SIQ migrator (with flaws)
- First release on pip under name `sakuragasaki46-suou`
- Improve sqlalchemy support

