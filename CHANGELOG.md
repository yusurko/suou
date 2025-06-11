# Changelog

## 0.3.0

- Add SQLAlchemy auth loaders i.e. `sqlalchemy.require_auth_base()`, `flask_sqlalchemy`.
  What auth loaders do is loading user token and signature into app
- Implement `UserSigner()`
- Improve JSON handling in `flask_restx`
- Add base2048 (i.e. [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)) codec
- Add `split_bits()`, `join_bits()`, `ltuple()`, `rtuple()`
- Add `markdown` extensions

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

