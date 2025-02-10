from starknet_py.net.models.chains import StarknetChainId

# Network settings
NODE_URL = "https://starknet-mainnet.public.blastapi.io"
CHAIN_ID = StarknetChainId.MAINNET

# Contract settings
ETH_CONTRACT_ADDRESS = (
    "0x49d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7"
)
CUSTOM_CONTRACT_ADDRESSES = {
    "STRK": {
        "address": "0x4718f5a0fc34cc1af16a1cdee98ffb20c31f5cd61d6ab07201858f4287c938d",
        "decimals": 18,
    },
    "USDC": {
        "address": "0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8",
        "decimals": 6,
    }
}

# Fee settings
FEE_BUFFER = 0.000034  # fee ETH buffer

# File paths
ADDRESSES_FILE = "addresses.txt"
PRIVATE_KEYS_FILE = "private_keys.txt"
RECIPIENTS_FILE = "recipients.txt"
OUTPUT_BALANCES_FILE = "output/balances.xlsx"
OUTPUT_TRANSACTIONS_FILE = "output/transactions.xlsx"

# Delay settings
DELAY_RANGE = [1, 5]  # sleep time range in seconds

# Transfer settings
TOKEN_TO_TRANSFER = (
    "ETH"  # or "STRK" for example (must be in CUSTOM_CONTRACT_ADDRESSES)
)
USE_ALL_BALANCE = True  # transfer all tokens
TRANSFER_AMOUNT_RANGE = [
    0.001,
    0.003,
]  # transfer amount range. Ignored if USE_ALL_BALANCE is True
