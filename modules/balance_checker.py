import asyncio
import random
from typing import Dict

import openpyxl
from starknet_py.contract import Contract
from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.signer.key_pair import KeyPair
from starknet_py.net.signer.stark_curve_signer import StarkCurveSigner

from config import (
    ADDRESSES_FILE,
    CHAIN_ID,
    CUSTOM_CONTRACT_ADDRESSES,
    DELAY_RANGE,
    ETH_CONTRACT_ADDRESS,
    NODE_URL,
    OUTPUT_BALANCES_FILE,
    PRIVATE_KEYS_FILE,
    RECIPIENTS_FILE,
)
from modules.wallet_loader import load_wallets


async def get_balances(address: str, private_key: str) -> Dict[str, int]:
    """
    Retrieve the ETH balance for a given Starknet address.

    This async function connects to a Starknet node and queries the ETH contract
    to get the balance for the specified address.

    Args:
        address (str): The Starknet address to check the balance for
        private_key (str): The private key associated with the address

    Returns:
        int: The ETH balance of the address in wei
    """
    client = FullNodeClient(NODE_URL)
    key_pair = KeyPair.from_private_key(private_key)
    signer = StarkCurveSigner(address, key_pair, CHAIN_ID)
    account = Account(
        address=address,
        client=client,
        signer=signer,
        chain=CHAIN_ID,
    )

    token_balances = {}

    # Get ETH balance
    eth_contract = await Contract.from_address(
        address=ETH_CONTRACT_ADDRESS, provider=account
    )
    eth_balance = (await eth_contract.functions["balanceOf"].call(account.address))[0]
    token_balances["ETH"] = eth_balance

    # Get other token balances if specified
    if CUSTOM_CONTRACT_ADDRESSES:
        for token_name, token_data in CUSTOM_CONTRACT_ADDRESSES.items():
            token_contract = await Contract.from_address(
                address=token_data["address"], provider=account
            )
            token_balance = (
                await token_contract.functions["balanceOf"].call(account.address)
            )[0]
            token_balances[token_name] = token_balance

    return token_balances


async def check_all_wallets():
    """
    Asynchronously checks and records wallet balances for multiple addresses.

    This function loads wallet information, creates an Excel workbook, and records ETH
    and custom token balances for each wallet address. The results are saved to an output file.

    Args:
        None

    Returns:
        None
    """
    wallets = load_wallets(
        ADDRESSES_FILE, PRIVATE_KEYS_FILE, RECIPIENTS_FILE, mode="balance"
    )
    wb = openpyxl.Workbook()
    ws = wb.create_sheet("Balances")
    wb.remove(wb.worksheets[0])  # Remove default sheet
    ws.append(["Address", "ETH", *CUSTOM_CONTRACT_ADDRESSES.keys()])

    print("Checking balances...")

    for address, data in wallets.items():
        balances = await get_balances(address, data["private_key"])

        formatted_balances = {}

        for token_name, balance in balances.items():
            if token_name == "ETH":
                formatted_balances[token_name] = balance / 10**18
            else:
                formatted_balances[token_name] = (
                    balance / 10 ** CUSTOM_CONTRACT_ADDRESSES[token_name]["decimals"]
                )

        ws.append([address, *formatted_balances.values()])
        await asyncio.sleep(random.uniform(*DELAY_RANGE))

    for column in ws.columns:
        length = max(len(str(cell.value)) for cell in column)
        ws.column_dimensions[column[0].column_letter].width = length + 2

    wb.save(OUTPUT_BALANCES_FILE)
    print(f"Balances saved to {OUTPUT_BALANCES_FILE}")


async def check_wallet(address: str, private_key: str) -> Dict[str, int]:
    """
    Checks the balances of various cryptocurrencies for a given wallet address.

    Args:
        address (str): The wallet address to check balances for.
        private_key (str): The private key associated with the wallet address.

    Returns:
        Dict[str, int]: A dictionary containing cryptocurrency symbols as keys and their respective balances as values.
    """
    return await get_balances(address, private_key)
