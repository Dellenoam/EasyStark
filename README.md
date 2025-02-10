# EasyStark 🚀

Script for various tasks in the StarkNet network

## Requirements

[![Python](https://img.shields.io/badge/python-%3E%3D3.10%20%3C3.13-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://www.python.org/)

## Features  

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Supported</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Balance checker</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Transfer ETH and other tokens from one wallet to another</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Wallet generator</td>
      <td><img src="https://img.shields.io/badge/TODO-in%20progress-orange" alt="TODO Badge"></td>
    </tr>
  </tbody>
</table>

## Settings

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <!-- Network Settings -->
    <tr>
      <td>NODE_URL</td>
      <td>URL of the StarkNet node to interact with.</td>
    </tr>
    <tr>
      <td>CHAIN_ID</td>
      <td>Identifier of the StarkNet network (e.g., MAINNET).</td>
    </tr>
    <!-- Contract Settings -->
    <tr>
      <td>ETH_CONTRACT_ADDRESS</td>
      <td>Contract address of the ETH token on StarkNet.</td>
    </tr>
    <tr>
      <td>CUSTOM_CONTRACT_ADDRESSES</td>
      <td>Dictionary containing custom token addresses and their decimals (e.g., STRK, USDC).</td>
    </tr>
    <!-- Fee Settings -->
    <tr>
      <td>FEE_BUFFER</td>
      <td>Buffer amount in ETH reserved to cover transaction fees.</td>
    </tr>
    <!-- File Paths -->
    <tr>
      <td>ADDRESSES_FILE</td>
      <td>File path containing wallet addresses.</td>
    </tr>
    <tr>
      <td>PRIVATE_KEYS_FILE</td>
      <td>File path containing private keys corresponding to the addresses.</td>
    </tr>
    <tr>
      <td>RECIPIENTS_FILE</td>
      <td>File path containing recipient addresses for transfers.</td>
    </tr>
    <tr>
      <td>OUTPUT_BALANCES_FILE</td>
      <td>Output file path to save wallet balances in Excel format.</td>
    </tr>
    <tr>
      <td>OUTPUT_TRANSACTIONS_FILE</td>
      <td>Output file path to save transaction details in Excel format.</td>
    </tr>
    <!-- Delay Settings -->
    <tr>
      <td>DELAY_RANGE</td>
      <td>Range (in seconds) for random delays between transactions.</td>
    </tr>
    <!-- Transfer Settings -->
    <tr>
      <td>TOKEN_TO_TRANSFER</td>
      <td>Token symbol to be transferred (e.g., ETH, STRK, USDC).</td>
    </tr>
    <tr>
      <td>USE_ALL_BALANCE</td>
      <td>True/False indicating whether to transfer the entire available balance.</td>
    </tr>
    <tr>
      <td>TRANSFER_AMOUNT_RANGE</td>
      <td>Range of transfer amounts (in ETH). Ignored if USE_ALL_BALANCE is True.</td>
    </tr>
  </tbody>
</table>

## How to install 📚

Before you begin, make sure you have meet the [requirements](#requirements). It's really IMPORTANT, without these requiremenets, you can NOT install our script.

### Linux manual installation

```shell
git clone https://github.com/Dellenoam/EasyStark.git
cd EasyStark
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install --only main
```

### Windows manual installation

```shell
git clone https://github.com/Dellenoam/EasyStark.git
cd EasyStark
python -m venv .venv
.venv\Scripts\activate
pip install poetry
poetry install --only main
```

### Configuration

You can configure the script by editing the `config.py` file. To learn more about options, see the [settings](#settings).

### How to import wallets

To import wallets into the script, you need to insert addresses of wallets into addresses.txt (starknet requires), private keys into private_keys.txt and recipients address into recipients.txt

## Run the script

Let's run the script!

### Using start.bat

You can run the script using start.bat script, just execute it.

### Manually

Before running the script, you ALWAYS need to activate the virtual environment and check for updates.

```shell
# Linux
source .venv\bin\activate
# Windows
.venv\Scripts\activate

# Linux/Windows
git pull
```

To run the script, use `python3 main.py` on Linux or `python main.py` on Windows.
