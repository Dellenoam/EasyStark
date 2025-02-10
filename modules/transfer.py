import asyncio
import random

import openpyxl
from aiohttp import ClientError
from starknet_py.contract import Contract
from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.signer.key_pair import KeyPair
from starknet_py.net.signer.stark_curve_signer import StarkCurveSigner

from config import (
    ADDRESSES_FILE,
    CHAIN_ID,
    CUSTOM_CONTRACT_ADDRESSES,
    ETH_CONTRACT_ADDRESS,
    FEE_BUFFER,
    NODE_URL,
    OUTPUT_TRANSACTIONS_FILE,
    PRIVATE_KEYS_FILE,
    RECIPIENTS_FILE,
    TOKEN_TO_TRANSFER,
    TRANSFER_AMOUNT_RANGE,
    USE_ALL_BALANCE,
)
from modules.balance_checker import check_wallet
from modules.wallet_loader import load_wallets


async def transfer_wallet(address: str, private_key: str, recipient: str) -> str | None:
    """
    Transfers wallet assets to a specified recipient on StarkNet.

    This async function handles the transfer of either ETH or a specified token from one wallet to another
    on the StarkNet network. It checks for sufficient balance before attempting the transfer and includes
    a buffer for transaction fees.

    Args:
        address (str): The sender's StarkNet wallet address.
        private_key (str): The private key of the sender's wallet.
        recipient (str): The recipient's StarkNet wallet address.

    Returns:
        None

    Raises:
        ClientError: If there's an error during the transaction execution.
    """
    balances = await check_wallet(address, private_key)

    available_eth_balance = balances["ETH"] / 10**18
    available_token_balance = (
        balances[TOKEN_TO_TRANSFER]
        / 10 ** CUSTOM_CONTRACT_ADDRESSES[TOKEN_TO_TRANSFER]["decimals"]
    )

    if available_eth_balance <= FEE_BUFFER:
        print(f"{address}: Insufficient ETH balance to cover fee. Skipping account...")
        return

    if TOKEN_TO_TRANSFER == "ETH":
        if available_eth_balance <= 0:
            print(f"{address}: ETH balance is zero. Skipping account...")
            return

        if USE_ALL_BALANCE:
            transfer_amount = available_eth_balance - FEE_BUFFER
            print(
                f"{address}: Using full ETH balance. Transferring: {transfer_amount}."
            )
        else:
            min_transfer, max_transfer = TRANSFER_AMOUNT_RANGE

            if available_eth_balance < min_transfer + FEE_BUFFER:
                print(
                    f"{address}: ETH balance ({available_eth_balance}) is insufficient for the minimum transfer. Skipping account..."
                )
                return

            max_possible_transfer = min(
                max_transfer, available_eth_balance - FEE_BUFFER
            )
            transfer_amount = random.uniform(min_transfer, max_possible_transfer)
            print(
                f"{address}: Selected ETH transfer amount: {transfer_amount} (with fee considered)."
            )

            transfer_amount = int(transfer_amount * 10**18)
    else:
        if available_token_balance <= 0:
            print(
                f"{address}: {TOKEN_TO_TRANSFER} balance is zero. Skipping account..."
            )
            return

        if USE_ALL_BALANCE:
            transfer_amount = available_token_balance
            print(
                f"{address}: Using full {TOKEN_TO_TRANSFER} balance: {transfer_amount}."
            )
        else:
            min_transfer, max_transfer = TRANSFER_AMOUNT_RANGE

            if available_token_balance < min_transfer:
                print(
                    f"{address}: {TOKEN_TO_TRANSFER} balance ({available_token_balance}) is less than the minimum transfer ({min_transfer}). Skipping account."
                )
                return

            max_possible_transfer = max(max_transfer, available_token_balance)
            transfer_amount = random.uniform(min_transfer, max_possible_transfer)
            print(
                f"{address}: Selected {TOKEN_TO_TRANSFER} transfer amount: {transfer_amount}."
            )

    transfer_amount_wei = int(transfer_amount * 10**18)

    client = FullNodeClient(NODE_URL)
    key_pair = KeyPair.from_private_key(private_key)
    signer = StarkCurveSigner(address, key_pair, CHAIN_ID)
    account = Account(
        address=address,
        client=client,
        signer=signer,
        chain=CHAIN_ID,
    )

    if TOKEN_TO_TRANSFER == "ETH":
        contract = await Contract.from_address(
            address=ETH_CONTRACT_ADDRESS, provider=account
        )
    else:
        contract = await Contract.from_address(
            address=CUSTOM_CONTRACT_ADDRESSES[TOKEN_TO_TRANSFER]["address"],
            provider=account,
        )

    transfer_call = contract.functions["transfer"].prepare_invoke_v1(
        int(recipient, 16), transfer_amount_wei
    )

    try:
        tx = await account.execute_v1(
            calls=[transfer_call],
            max_fee=int(FEE_BUFFER * 10**18),
        )
        tx_link = f"https://starkscan.co/tx/{hex(tx.transaction_hash)}"
        print(f"Transaction for {address} sent. TX: {tx_link}")
    except ClientError as error:
        tx_link = "N/A"
        print(f"Error for {address}: {error}")

    return tx_link


async def transfer_all_wallets() -> None:
    """
    Executes transfers for all wallets loaded from configuration files.

    This asynchronous function loads wallet data and performs transfers for each wallet sequentially.
    Between each transfer, it introduces a random delay of 10-20 seconds.

    Args:
        None

    Returns:
        None
    """
    wallets = load_wallets(
        ADDRESSES_FILE, PRIVATE_KEYS_FILE, RECIPIENTS_FILE, mode="transfer"
    )

    completed_txs = {}

    for address, data in wallets.items():
        tx_link = await transfer_wallet(address, data["private_key"], data["recipient"])
        completed_txs[address] = tx_link

        await asyncio.sleep(random.randint(10, 20))

    wb = openpyxl.Workbook()
    ws = wb.create_sheet("Transactions")
    wb.remove(wb.worksheets[0])  # Remove default sheet
    ws.append(["Address", "Transaction Link"])

    for address, tx_link in completed_txs.items():
        ws.append([address, tx_link])

    for column in ws.columns:
        length = max(len(str(cell.value)) for cell in column)
        ws.column_dimensions[column[0].column_letter].width = length + 2

    wb.save(OUTPUT_TRANSACTIONS_FILE)
    print(f"Transactions saved to {OUTPUT_TRANSACTIONS_FILE}")
