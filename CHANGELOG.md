# Changelog

## 0.3.4

- Bug fixes in `.flask_sqlalchemy` and `.sqlalchemy` — `require_auth()` is unusable before this point!

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

