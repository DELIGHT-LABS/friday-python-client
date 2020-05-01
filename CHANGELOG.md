Changelog
=========

This log documents all public API breaking backwards incompatible changes.

0.4.1
----

- Prepare CI with real Hdac mainnet node

0.4.0
----

- REST API updated according to classify hdac specific endpoint and general contract
- Update against request format changes

0.3.2
----

- REST API updated according to readable ID feature integration

0.3.1
-----

- Fixed parameter of transfer `token_owner_address` -> `token_contract_address`

0.3.0
-----

- Getting Mnemonic words is available in wallet generation

0.2.0
-----

- Fix parameters of transfer

0.1.3
-----

- Get auth info
- Apply account number & sequence by REST request, not manually input

0.1.2
-----

- Update `gas` & `memo` in every requests

0.1.1
-----

- `fee` Parameter added to each tx

0.1.0
-----

- Forked project from hukkinj1/cosmospy
- Added
  - Code for address generation and transaction signing based on RESTful route
  - Modified test
