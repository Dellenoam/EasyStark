def load_wallets(
    addresses_file: str, private_keys_file: str, recipients_file: str, mode: str
) -> dict:
    """
    Loads wallet data from specified files and returns a dictionary containing wallet information.

    This function reads wallet addresses, private keys, and recipient addresses from their respective files
    and constructs a dictionary mapping each wallet address to its corresponding private key and recipient.
    The function ensures that the number of addresses matches the number of private keys, and if in transfer
    mode, also checks that the number of recipients matches.

    Args:
        addresses_file (str): Path to the file containing wallet addresses.
        private_keys_file (str): Path to the file containing private keys corresponding to the wallet addresses.
        recipients_file (str): Path to the file containing recipient addresses.
        mode (str): Operation mode, either "balance" or "transfer". In "balance" mode, recipients are not used.

    Returns:
        dict: A dictionary with wallet addresses as keys and their private keys and recipients as values.

    Raises:
        ValueError: If the number of addresses and private keys do not match, or if in transfer mode,
                    the number of recipients and addresses do not match.
    """

    wallets = {}

    with open(addresses_file, encoding="utf-8") as f:
        addresses = [line.strip() for line in f if line.strip()]
    with open(private_keys_file, encoding="utf-8") as f:
        private_keys = [line.strip() for line in f if line.strip()]
    with open(recipients_file, encoding="utf-8") as f:
        recipients = [line.strip() for line in f if line.strip()]

    if len(addresses) != len(private_keys):
        raise ValueError("Number of wallets and keys do not match")

    if mode != "balance" and len(private_keys) != len(recipients):
        raise ValueError("Number of wallets, keys and recipients do not match")

    wallets = {}
    for i in range(len(addresses)):
        wallets[addresses[i]] = {
            "private_key": private_keys[i],
            "recipient": recipients[i] if mode != "balance" else None,
        }

    return wallets
