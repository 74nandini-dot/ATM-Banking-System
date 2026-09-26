import json
import os
import hashlib
from decimal import Decimal

from users import DEFAULT_ACCOUNTS


DATA_FOLDER = "data"
DATA_FILE = os.path.join(
    DATA_FOLDER,
    "accounts.json"
)


# ==========================================
# HASH PIN
# ==========================================

def hash_pin(pin):

    return hashlib.sha256(
        pin.encode()
    ).hexdigest()


# ==========================================
# DECIMAL TO FLOAT
# ==========================================

def decimal_to_float(value):

    return float(
        Decimal(
            str(value)
        )
    )


# ==========================================
# LOAD ACCOUNTS
# ==========================================

def load_accounts():

    if not os.path.exists(DATA_FOLDER):

        os.makedirs(DATA_FOLDER)

    if not os.path.exists(DATA_FILE):

        accounts = {}

        for account_number, account in DEFAULT_ACCOUNTS.items():

            account_copy = account.copy()

            account_copy["pin"] = hash_pin(
                account_copy["pin"]
            )

            account_copy["balance"] = decimal_to_float(
                account_copy["balance"]
            )

            account_copy["daily_withdrawal"] = decimal_to_float(
                account_copy.get(
                    "daily_withdrawal",
                    0
                )
            )

            accounts[account_number] = account_copy

        with open(
            DATA_FILE,
            "w"
        ) as file:

            json.dump(
                accounts,
                file,
                indent=4
            )

        return accounts


    with open(
        DATA_FILE,
        "r"
    ) as file:

        accounts = json.load(file)


    return accounts


# ==========================================
# SAVE ACCOUNTS
# ==========================================

def save_accounts(accounts):

    if not os.path.exists(DATA_FOLDER):

        os.makedirs(DATA_FOLDER)


    clean_accounts = {}


    for account_number, account in accounts.items():

        account_copy = account.copy()


        # ------------------------------------------
        # BALANCE
        # ------------------------------------------

        account_copy["balance"] = decimal_to_float(
            account_copy.get(
                "balance",
                0
            )
        )


        # ------------------------------------------
        # DAILY WITHDRAWAL
        # ------------------------------------------

        account_copy["daily_withdrawal"] = decimal_to_float(
            account_copy.get(
                "daily_withdrawal",
                0
            )
        )


        # ------------------------------------------
        # TRANSACTIONS
        # ------------------------------------------

        clean_transactions = []


        for transaction in account_copy.get(
            "transactions",
            []
        ):

            if not isinstance(
                transaction,
                dict
            ):

                continue


            transaction_copy = transaction.copy()


            transaction_copy["amount"] = decimal_to_float(
                transaction_copy.get(
                    "amount",
                    0
                )
            )


            transaction_copy["balance"] = decimal_to_float(
                transaction_copy.get(
                    "balance",
                    0
                )
            )


            clean_transactions.append(
                transaction_copy
            )


        account_copy["transactions"] = (
            clean_transactions
        )


        clean_accounts[account_number] = (
            account_copy
        )


    # ------------------------------------------
    # SAVE JSON
    # ------------------------------------------

    with open(
        DATA_FILE,
        "w"
    ) as file:

        json.dump(
            clean_accounts,
            file,
            indent=4
        )