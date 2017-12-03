# The Sparkles Crypto currency
A **semi-distributed crypto currency** built with Python and WebSockets

## Installation

Download the `deploy` branch or clone it

Install the deps

``
pip install -r requirements.txt
``

## Running the Wallet

Navigate to the `node` folder

``
cd ./node
``

Generate your wallet address

``
python generate_keys.py
``

Or if you already generated your keys. Move them to the `./keys` folder as `public.pem` and `secret.pem`

Run the wallet

``
python wallet_client.py
``

## Running the Miner

Navigate to the `mine` folder

Generate you wallet address

``` python generate_keys.py ```

Or if you already generated your keys. Move them to the `./keys` folder as `public.pem` and `secret.pem`

Run the miner

``
python miner_client.py
``

## Issues

* Not fully P2P
* Look out for block overload
* Not worth anything (yet)

## Contribute

If you find an issue or bugs, feel free to create an issue or create a pull request

Contributions are greatly appreciated!

---
LICENSE: MIT

Created by Michael Navazhylau (Mechasparrow)
