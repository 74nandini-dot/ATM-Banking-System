import hashlib
import time

from database import load_accounts, save_accounts


# ==========================================
# ADMIN LOGIN DETAILS
# ==========================================

ADMIN_ID = "admin"
ADMIN_PASSWORD = "admin123"


# ==========================================
# ADMIN LOGIN
# ==========================================

def admin_login():

    print("\n========================================")
    print("            ADMIN LOGIN")
    print("========================================")

    admin_id = input("Admin ID: ")
    admin_password = input("Admin Password: ")

    password_hash = hashlib.sha256(
        admin_password.encode()
    ).hexdigest()

    correct_hash = hashlib.sha256(
        ADMIN_PASSWORD.encode()
    ).hexdigest()

    if (
        admin_id == ADMIN_ID
        and password_hash == correct_hash
    ):

        print("\nAdmin login successful!")
        return True

    print("\nInvalid Admin ID or Password.")
    return False


# ==========================================
# ADMIN DASHBOARD
# ==========================================

def admin_dashboard(accounts):

    print("\n========================================")
    print("          BANK ADMIN DASHBOARD")
    print("========================================")

    total_accounts = len(accounts)
    active_accounts = 0
    locked_accounts = 0
    total_balance = 0
    total_transactions = 0

    highest_balance = -1
    highest_balance_account = ""
    highest_balance_name = ""

    for account_number, account in accounts.items():

        balance = account.get("balance", 0)

        total_balance += balance

        transactions = account.get(
            "transactions",
            []
        )

        total_transactions += len(transactions)

        lock_until = account.get(
            "lock_until",
            0
        )

        if time.time() < lock_until:
            locked_accounts += 1
        else:
            active_accounts += 1

        if balance > highest_balance:

            highest_balance = balance
            highest_balance_account = account_number

            highest_balance_name = account.get(
                "name",
                "Unknown"
            )

    print(
        "Total Accounts       :",
        total_accounts
    )

    print(
        "Active Accounts      :",
        active_accounts
    )

    print(
        "Locked Accounts      :",
        locked_accounts
    )

    print(
        "Total Bank Balance   : ₹",
        total_balance
    )

    print(
        "Total Transactions   :",
        total_transactions
    )

    print("----------------------------------------")

    if total_accounts > 0:

        print(
            "Highest Balance      : ₹",
            highest_balance
        )

        print(
            "Account Holder       :",
            highest_balance_name
        )

        print(
            "Account Number       :",
            highest_balance_account
        )

    else:

        print("No accounts available.")

    print("========================================")


# ==========================================
# VIEW ALL ACCOUNTS
# ==========================================

def view_all_accounts(accounts):

    print("\n========================================")
    print("             ALL ACCOUNTS")
    print("========================================")

    if len(accounts) == 0:

        print("No accounts available.")
        return

    for account_number, account in accounts.items():

        print("\nAccount Number :", account_number)

        print(
            "Account Holder :",
            account["name"]
        )

        print(
            "Balance        : ₹",
            account["balance"]
        )

        print(
            "Transactions   :",
            len(account.get("transactions", []))
        )

        failed_attempts = account.get(
            "failed_attempts",
            0
        )

        lock_until = account.get(
            "lock_until",
            0
        )

        if time.time() < lock_until:
            status = "LOCKED"
        else:
            status = "ACTIVE"

        print("Status         :", status)

        print(
            "Failed Attempts:",
            failed_attempts
        )

        print("----------------------------------------")


# ==========================================
# SEARCH ACCOUNT
# ==========================================

def search_account(accounts):

    account_number = input(
        "\nEnter account number: "
    ).strip()

    if account_number not in accounts:

        print("\nAccount not found.")
        return

    account = accounts[account_number]

    print("\n========================================")
    print("           ACCOUNT DETAILS")
    print("========================================")

    print(
        "Account Number :",
        account_number
    )

    print(
        "Account Holder :",
        account["name"]
    )

    print(
        "Balance        : ₹",
        account["balance"]
    )

    print(
        "Transactions   :",
        len(account.get("transactions", []))
    )

    lock_until = account.get(
        "lock_until",
        0
    )

    if time.time() < lock_until:

        remaining = int(
            lock_until - time.time()
        ) + 1

        print("Status         : LOCKED")

        print(
            "Unlocks in     :",
            remaining,
            "seconds"
        )

    else:

        print("Status         : ACTIVE")

    print("========================================")


# ==========================================
# UNLOCK ACCOUNT
# ==========================================

def unlock_account(accounts):

    account_number = input(
        "\nEnter account number to unlock: "
    ).strip()

    if account_number not in accounts:

        print("\nAccount not found.")
        return

    account = accounts[account_number]

    account["failed_attempts"] = 0
    account["lock_until"] = 0

    save_accounts(accounts)

    print("\nAccount unlocked successfully!")


# ==========================================
# CREATE NEW ACCOUNT
# ==========================================

def create_account(accounts):

    print("\n========================================")
    print("          CREATE NEW ACCOUNT")
    print("========================================")

    account_number = input(
        "Enter new account number: "
    ).strip()

    if not account_number.isdigit():

        print(
            "\nAccount number must contain digits only."
        )

        return

    if account_number in accounts:

        print("\nAccount already exists.")
        return

    name = input(
        "Enter account holder name: "
    ).strip()

    if not name:

        print(
            "\nAccount holder name cannot be empty."
        )

        return

    pin = input(
        "Create 4-digit PIN: "
    ).strip()

    if len(pin) != 4 or not pin.isdigit():

        print(
            "\nPIN must contain exactly 4 digits."
        )

        return

    confirm_pin = input(
        "Confirm PIN: "
    ).strip()

    if pin != confirm_pin:

        print("\nPINs do not match.")
        return

    try:

        balance = float(
            input("Enter initial balance: ₹ ")
        )

    except ValueError:

        print("\nInvalid balance.")
        return

    if balance < 0:

        print(
            "\nBalance cannot be negative."
        )

        return

    hashed_pin = hashlib.sha256(
        pin.encode()
    ).hexdigest()

    accounts[account_number] = {

        "name": name,

        "pin": hashed_pin,

        "balance": balance,

        "transactions": [],

        "daily_withdrawal": 0,

        "last_withdrawal_date": "",

        "failed_attempts": 0,

        "lock_until": 0
    }

    save_accounts(accounts)

    print("\n========================================")
    print("       ACCOUNT CREATED SUCCESSFULLY")
    print("========================================")

    print(
        "Account Number :",
        account_number
    )

    print(
        "Account Holder :",
        name
    )

    print(
        "Initial Balance:",
        "₹",
        balance
    )

    print("========================================")


# ==========================================
# DELETE ACCOUNT
# ==========================================

def delete_account(accounts):

    print("\n========================================")
    print("           DELETE ACCOUNT")
    print("========================================")

    account_number = input(
        "Enter account number to delete: "
    ).strip()

    if account_number not in accounts:

        print("\nAccount not found.")
        return

    account = accounts[account_number]

    print(
        "\nAccount Holder:",
        account["name"]
    )

    print(
        "Current Balance: ₹",
        account["balance"]
    )

    confirmation = input(
        "\nType DELETE to confirm: "
    ).strip()

    if confirmation != "DELETE":

        print(
            "\nAccount deletion cancelled."
        )

        return

    del accounts[account_number]

    save_accounts(accounts)

    print(
        "\nAccount deleted successfully!"
    )


# ==========================================
# VIEW ALL TRANSACTIONS
# ==========================================

def view_all_transactions(accounts):

    print("\n========================================")
    print("          ALL TRANSACTIONS")
    print("========================================")

    total_transactions = 0

    for account_number, account in accounts.items():

        transactions = account.get(
            "transactions",
            []
        )

        if len(transactions) == 0:
            continue

        print("\n----------------------------------------")

        print(
            "Account:",
            account_number
        )

        print(
            "Holder :",
            account["name"]
        )

        print("----------------------------------------")

        for transaction in transactions:

            if not isinstance(transaction, dict):
                continue

            total_transactions += 1

            print(
                "Transaction ID :",
                transaction.get(
                    "transaction_id",
                    "N/A"
                )
            )

            print(
                "Date & Time    :",
                transaction.get("date_time", "")
            )

            print(
                "Type           :",
                transaction.get("type", "")
            )

            print(
                "Amount         : ₹",
                transaction.get("amount", 0)
            )

            print(
                "Balance        : ₹",
                transaction.get("balance", 0)
            )

            if transaction.get("details"):

                print(
                    "Details        :",
                    transaction["details"]
                )

            print("----------------------------------------")

    if total_transactions == 0:

        print("\nNo transactions available.")

    else:

        print(
            "\nTotal Transactions:",
            total_transactions
        )

    print("========================================")


# ==========================================
# ACCOUNT TRANSACTION HISTORY
# ==========================================

def account_transaction_history(accounts):

    print("\n========================================")
    print("       ACCOUNT TRANSACTION HISTORY")
    print("========================================")

    account_number = input(
        "Enter account number: "
    ).strip()

    if account_number not in accounts:

        print("\nAccount not found.")
        return

    account = accounts[account_number]

    transactions = account.get(
        "transactions",
        []
    )

    print(
        "\nAccount Holder :",
        account["name"]
    )

    print(
        "Account Number :",
        account_number
    )

    print(
        "Current Balance:",
        "₹",
        account["balance"]
    )

    print(
        "Total Transactions:",
        len(transactions)
    )

    print("----------------------------------------")

    if len(transactions) == 0:

        print("No transactions available.")
        return

    for transaction in transactions:

        if not isinstance(transaction, dict):
            continue

        print(
            "\nTransaction ID :",
            transaction.get(
                "transaction_id",
                "N/A"
            )
        )

        print(
            "Date & Time    :",
            transaction.get("date_time", "")
        )

        print(
            "Type           :",
            transaction.get("type", "")
        )

        print(
            "Amount         : ₹",
            transaction.get("amount", 0)
        )

        print(
            "Balance        : ₹",
            transaction.get("balance", 0)
        )

        if transaction.get("details"):

            print(
                "Details        :",
                transaction["details"]
            )

        print("----------------------------------------")


# ==========================================
# SHOW TRANSACTIONS BY TYPE
# ==========================================

def show_transactions_by_type(
    accounts,
    transaction_type
):

    print("\n========================================")

    print(
        "       ",
        transaction_type,
        "TRANSACTIONS"
    )

    print("========================================")

    found = False
    total_amount = 0
    total_count = 0

    for account_number, account in accounts.items():

        transactions = account.get(
            "transactions",
            []
        )

        for transaction in transactions:

            if not isinstance(transaction, dict):
                continue

            if transaction.get("type") != transaction_type:
                continue

            found = True
            total_count += 1

            amount = transaction.get(
                "amount",
                0
            )

            total_amount += amount

            print(
                "\nAccount Number :",
                account_number
            )

            print(
                "Account Holder :",
                account.get("name", "Unknown")
            )

            print(
                "Transaction ID :",
                transaction.get(
                    "transaction_id",
                    "N/A"
                )
            )

            print(
                "Date & Time    :",
                transaction.get("date_time", "")
            )

            print(
                "Type           :",
                transaction.get("type", "")
            )

            print(
                "Amount         : ₹",
                amount
            )

            print(
                "Balance        : ₹",
                transaction.get("balance", 0)
            )

            if transaction.get("details"):

                print(
                    "Details        :",
                    transaction["details"]
                )

            print("----------------------------------------")

    if not found:

        print("\nNo matching transactions found.")

    else:

        print(
            "\nTotal Transactions:",
            total_count
        )

        print(
            "Total Amount      : ₹",
            total_amount
        )

    print("========================================")


# ==========================================
# ADMIN TRANSACTION FILTER
# ==========================================

def filter_admin_transactions(accounts):

    while True:

        print("\n========================================")
        print("       ADMIN TRANSACTION FILTER")
        print("========================================")

        print("1. All Transactions")
        print("2. Deposits")
        print("3. Withdrawals")
        print("4. Transfers")
        print("5. Received Money")
        print("6. Search by Account Number")
        print("7. Back")

        choice = input(
            "\nEnter your choice: "
        )

        if choice == "1":

            view_all_transactions(accounts)

        elif choice == "2":

            show_transactions_by_type(
                accounts,
                "DEPOSIT"
            )

        elif choice == "3":

            show_transactions_by_type(
                accounts,
                "WITHDRAW"
            )

        elif choice == "4":

            show_transactions_by_type(
                accounts,
                "TRANSFER"
            )

        elif choice == "5":

            show_transactions_by_type(
                accounts,
                "RECEIVED"
            )

        elif choice == "6":

            account_number = input(
                "\nEnter account number: "
            ).strip()

            if account_number not in accounts:

                print("\nAccount not found.")

            else:

                account = accounts[account_number]

                print(
                    "\n========================================"
                )

                print(
                    "       ACCOUNT TRANSACTION HISTORY"
                )

                print(
                    "========================================"
                )

                print(
                    "Account Holder :",
                    account["name"]
                )

                print(
                    "Account Number :",
                    account_number
                )

                print(
                    "Current Balance: ₹",
                    account["balance"]
                )

                transactions = account.get(
                    "transactions",
                    []
                )

                if len(transactions) == 0:

                    print(
                        "\nNo transactions available."
                    )

                else:

                    for transaction in transactions:

                        if not isinstance(
                            transaction,
                            dict
                        ):
                            continue

                        print(
                            "\nTransaction ID :",
                            transaction.get(
                                "transaction_id",
                                "N/A"
                            )
                        )

                        print(
                            "Date & Time    :",
                            transaction.get(
                                "date_time",
                                ""
                            )
                        )

                        print(
                            "Type           :",
                            transaction.get(
                                "type",
                                ""
                            )
                        )

                        print(
                            "Amount         : ₹",
                            transaction.get(
                                "amount",
                                0
                            )
                        )

                        print(
                            "Balance        : ₹",
                            transaction.get(
                                "balance",
                                0
                            )
                        )

                        if transaction.get("details"):

                            print(
                                "Details        :",
                                transaction["details"]
                            )

                        print(
                            "----------------------------------------"
                        )

                print(
                    "========================================"
                )

        elif choice == "7":

            break

        else:

            print("\nInvalid choice.")


# ==========================================
# ADMIN MENU
# ==========================================

def admin_menu():

    accounts = load_accounts()

    while True:

        print("\n========================================")
        print("              ADMIN PANEL")
        print("========================================")

        print("1. Dashboard")
        print("2. View All Accounts")
        print("3. Search Account")
        print("4. Unlock Account")
        print("5. Create New Account")
        print("6. Delete Account")
        print("7. View All Transactions")
        print("8. Account Transaction History")
        print("9. Transaction Search & Filter")
        print("10. Logout")

        choice = input(
            "\nEnter your choice: "
        )

        if choice == "1":

            admin_dashboard(accounts)

        elif choice == "2":

            view_all_accounts(accounts)

        elif choice == "3":

            search_account(accounts)

        elif choice == "4":

            unlock_account(accounts)

        elif choice == "5":

            create_account(accounts)

        elif choice == "6":

            delete_account(accounts)

        elif choice == "7":

            view_all_transactions(accounts)

        elif choice == "8":

            account_transaction_history(accounts)

        elif choice == "9":

            filter_admin_transactions(accounts)

        elif choice == "10":

            print(
                "\nAdmin logged out successfully."
            )

            break

        else:

            print(
                "\nInvalid choice."
            )


# ==========================================
# START ADMIN PANEL
# ==========================================

if __name__ == "__main__":

    if admin_login():

        admin_menu()