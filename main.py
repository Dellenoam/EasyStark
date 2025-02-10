import asyncio

from modules.balance_checker import check_all_wallets
from modules.transfer import transfer_all_wallets


def main():
    print("\nSelect operation mode:")
    print("1. Check balances")
    print("2. Transfer tokens")
    choice = input("Enter your choice (1-2): ")

    mode = "balance" if choice == "1" else "transfer"

    if mode == "balance":
        asyncio.run(check_all_wallets())
    elif mode == "transfer":
        asyncio.run(transfer_all_wallets())


if __name__ == "__main__":
    main()
