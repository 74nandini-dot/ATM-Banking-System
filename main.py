import hashlib
import time

from decimal import Decimal, InvalidOperation
from database import load_accounts, save_accounts
from transactions import create_transaction

from utils import (
    format_transaction,
    print_receipt,
    save_receipt,
    print_account_statement,
    filter_transactions,
    export_statement_csv
)

from getpass import getpass
from datetime import datetime


print("================================")
print("       ATM BANKING SYSTEM")
print("================================")


# ==========================================
# LOAD ACCOUNT DATA
# ==========================================

accounts = load_accounts()


# ==========================================
# ADD SECURITY FIELDS
# ==========================================

for account in accounts.values():

    if "failed_attempts" not in account:
        account["failed_attempts"] = 0

    if "lock_until" not in account:
        account["lock_until"] = 0


save_accounts(accounts)


# ==========================================
# DAILY WITHDRAWAL SETTINGS
# ==========================================

DAILY_WITHDRAWAL_LIMIT = Decimal("20000")

today = datetime.now().strftime("%d-%m-%Y")


for account in accounts.values():

    if "daily_withdrawal" not in account:
        account["daily_withdrawal"] = 0

    if "last_withdrawal_date" not in account:
        account["last_withdrawal_date"] = ""

    if account["last_withdrawal_date"] != today:

        account["daily_withdrawal"] = 0
        account["last_withdrawal_date"] = today


save_accounts(accounts)


# ==========================================
# SECURITY SETTINGS
# ==========================================

MAX_LOGIN_ATTEMPTS = 3
LOCK_TIME = 60


# ==========================================
# LOGIN SYSTEM
# ==========================================

while True:

    user_account = input(
        "\nEnter Account Number: "
    )

    # ------------------------------------------
    # CHECK ACCOUNT NUMBER
    # ------------------------------------------

    if user_account not in accounts:

        print("\nAccount not found.")
        continue


    account = accounts[user_account]


    # ------------------------------------------
    # CHECK ACCOUNT LOCK
    # ------------------------------------------

    current_time = time.time()
    lock_until = account.get("lock_until", 0)


    if current_time < lock_until:

        remaining_seconds = int(
            lock_until - current_time
        ) + 1

        print("\n========================================")
        print("          ACCOUNT TEMPORARILY LOCKED")
        print("========================================")

        print(
            "Please try again after",
            remaining_seconds,
            "seconds."
        )

        print("========================================")

        continue


    # ------------------------------------------
    # RESET EXPIRED LOCK
    # ------------------------------------------

    if lock_until != 0:

        account["lock_until"] = 0
        account["failed_attempts"] = 0

        save_accounts(accounts)


    # ==========================================
    # PIN VERIFICATION
    # ==========================================

    while account["failed_attempts"] < MAX_LOGIN_ATTEMPTS:

        user_pin = getpass(
            "Enter PIN: "
        )

        user_pin_hash = hashlib.sha256(
            user_pin.encode()
        ).hexdigest()


        # ------------------------------------------
        # CORRECT PIN
        # ------------------------------------------

        if account["pin"] == user_pin_hash:

            account["failed_attempts"] = 0

            save_accounts(accounts)

            name = account["name"]

            print("\nLogin Successful!")
            print("Welcome,", name)
            print("Account Number:", user_account)


            # ==========================================
            # ATM MENU
            # ==========================================

            while True:

                print("\n========== ATM MENU ==========")
                print("1. Check Balance")
                print("2. Withdraw Cash")
                print("3. Deposit Cash")
                print("4. Transfer Money")
                print("5. Transaction History & Filter")
                print("6. Export Statement to CSV")
                print("7. Change PIN")
                print("8. Logout")

                choice = input(
                    "\nEnter your choice: "
                )


                # ==========================================
                # CHECK BALANCE
                # ==========================================

                if choice == "1":

                    balance = accounts[
                        user_account
                    ]["balance"]

                    print(
                        "\n========== ACCOUNT BALANCE =========="
                    )

                    print(
                        "Account Holder:",
                        name
                    )

                    print(
                        "Account Number:",
                        user_account
                    )

                    print(
                        "Current Balance: ₹",
                        Decimal(str(balance))
                    )


                # ==========================================
                # WITHDRAW CASH
                # ==========================================

                elif choice == "2":

                    try:

                        amount = Decimal(
                            input(
                                "\nEnter withdrawal amount: ₹ "
                            ).strip()
                        )

                        balance = Decimal(
                            str(
                                accounts[
                                    user_account
                                ]["balance"]
                            )
                        )

                        daily_withdrawal = Decimal(
                            str(
                                accounts[
                                    user_account
                                ]["daily_withdrawal"]
                            )
                        )

                        remaining_limit = (
                            DAILY_WITHDRAWAL_LIMIT
                            - daily_withdrawal
                        )


                        if amount <= 0:

                            print(
                                "\nInvalid withdrawal amount."
                            )


                        elif amount > balance:

                            print(
                                "\nInsufficient balance."
                            )

                            print(
                                "Your current balance is: ₹",
                                balance
                            )


                        elif amount > remaining_limit:

                            print(
                                "\nDaily withdrawal "
                                "limit exceeded."
                            )

                            print(
                                "Daily limit: ₹",
                                DAILY_WITHDRAWAL_LIMIT
                            )

                            print(
                                "Already withdrawn today: ₹",
                                daily_withdrawal
                            )

                            print(
                                "Remaining limit: ₹",
                                remaining_limit
                            )


                        else:

                            accounts[
                                user_account
                            ]["balance"] = (
                                balance - amount
                            )


                            accounts[
                                user_account
                            ]["daily_withdrawal"] = (
                                daily_withdrawal + amount
                            )


                            accounts[
                                user_account
                            ]["last_withdrawal_date"] = today


                            new_balance = (
                                balance - amount
                            )


                            transaction = create_transaction(
                                "WITHDRAW",
                                float(amount),
                                float(new_balance),
                                "Cash withdrawal"
                            )


                            accounts[
                                user_account
                            ]["transactions"].append(
                                transaction
                            )


                            save_accounts(accounts)


                            new_remaining_limit = (
                                DAILY_WITHDRAWAL_LIMIT
                                - (
                                    daily_withdrawal
                                    + amount
                                )
                            )


                            print(
                                "\nWithdrawal successful!"
                            )

                            print(
                                "Amount withdrawn: ₹",
                                amount
                            )

                            print(
                                "Remaining balance: ₹",
                                new_balance
                            )

                            print(
                                "Today's remaining "
                                "withdrawal limit: ₹",
                                new_remaining_limit
                            )


                            print_receipt(
                                user_account,
                                name,
                                transaction
                            )


                            save_receipt(
                                user_account,
                                name,
                                transaction
                            )


                    except (
                        InvalidOperation,
                        ValueError
                    ):

                        print("\nInvalid input!")

                        print(
                            "Please enter a valid number."
                        )


                # ==========================================
                # DEPOSIT CASH
                # ==========================================

                elif choice == "3":

                    try:

                        amount = Decimal(
                            input(
                                "\nEnter deposit amount: ₹ "
                            ).strip()
                        )


                        if amount <= 0:

                            print(
                                "\nInvalid deposit amount."
                            )


                        else:

                            current_balance = Decimal(
                                str(
                                    accounts[
                                        user_account
                                    ]["balance"]
                                )
                            )


                            new_balance = (
                                current_balance
                                + amount
                            )


                            accounts[
                                user_account
                            ]["balance"] = new_balance


                            transaction = create_transaction(
                                "DEPOSIT",
                                float(amount),
                                float(new_balance),
                                "Cash deposit"
                            )


                            accounts[
                                user_account
                            ]["transactions"].append(
                                transaction
                            )


                            save_accounts(accounts)


                            print(
                                "\nDeposit successful!"
                            )

                            print(
                                "Amount deposited: ₹",
                                amount
                            )

                            print(
                                "Updated balance: ₹",
                                new_balance
                            )


                            print_receipt(
                                user_account,
                                name,
                                transaction
                            )


                            save_receipt(
                                user_account,
                                name,
                                transaction
                            )


                    except (
                        InvalidOperation,
                        ValueError
                    ):

                        print("\nInvalid input!")

                        print(
                            "Please enter a valid number."
                        )


                # ==========================================
                # TRANSFER MONEY
                # ==========================================

                elif choice == "4":

                    print(
                        "\n========== MONEY TRANSFER =========="
                    )

                    receiver = input(
                        "Enter receiver account number: "
                    )


                    if receiver not in accounts:

                        print(
                            "\nReceiver account not found."
                        )


                    elif receiver == user_account:

                        print(
                            "\nYou cannot transfer money "
                            "to your own account."
                        )


                    else:

                        try:

                            amount = Decimal(
                                input(
                                    "Enter transfer amount: ₹ "
                                ).strip()
                            )


                            sender_balance = Decimal(
                                str(
                                    accounts[
                                        user_account
                                    ]["balance"]
                                )
                            )


                            if amount <= 0:

                                print(
                                    "\nInvalid transfer amount."
                                )


                            elif amount > sender_balance:

                                print(
                                    "\nInsufficient balance."
                                )

                                print(
                                    "Your current balance is: ₹",
                                    sender_balance
                                )


                            else:

                                receiver_balance = Decimal(
                                    str(
                                        accounts[
                                            receiver
                                        ]["balance"]
                                    )
                                )


                                sender_new_balance = (
                                    sender_balance
                                    - amount
                                )


                                receiver_new_balance = (
                                    receiver_balance
                                    + amount
                                )


                                accounts[
                                    user_account
                                ]["balance"] = (
                                    sender_new_balance
                                )


                                accounts[
                                    receiver
                                ]["balance"] = (
                                    receiver_new_balance
                                )


                                receiver_name = accounts[
                                    receiver
                                ]["name"]


                                sender_transaction = (
                                    create_transaction(
                                        "TRANSFER",
                                        float(amount),
                                        float(sender_new_balance),
                                        f"Transferred to "
                                        f"{receiver_name} "
                                        f"({receiver})"
                                    )
                                )


                                accounts[
                                    user_account
                                ]["transactions"].append(
                                    sender_transaction
                                )


                                receiver_transaction = (
                                    create_transaction(
                                        "RECEIVED",
                                        float(amount),
                                        float(receiver_new_balance),
                                        f"Received from "
                                        f"{name} "
                                        f"({user_account})"
                                    )
                                )


                                accounts[
                                    receiver
                                ]["transactions"].append(
                                    receiver_transaction
                                )


                                save_accounts(accounts)


                                print(
                                    "\nTransfer successful!"
                                )

                                print(
                                    "Amount transferred: ₹",
                                    amount
                                )

                                print(
                                    "Receiver:",
                                    receiver_name
                                )

                                print(
                                    "Receiver Account:",
                                    receiver
                                )

                                print(
                                    "Remaining balance: ₹",
                                    sender_new_balance
                                )


                                print_receipt(
                                    user_account,
                                    name,
                                    sender_transaction
                                )


                                save_receipt(
                                    user_account,
                                    name,
                                    sender_transaction
                                )


                        except (
                            InvalidOperation,
                            ValueError
                        ):

                            print("\nInvalid input!")

                            print(
                                "Please enter a valid number."
                            )


                # ==========================================
                # TRANSACTION HISTORY & FILTER
                # ==========================================

                elif choice == "5":

                    while True:

                        print(
                            "\n========================================"
                        )

                        print(
                            "       TRANSACTION HISTORY & FILTER"
                        )

                        print(
                            "========================================"
                        )

                        print("1. All Transactions")
                        print("2. Deposits")
                        print("3. Withdrawals")
                        print("4. Transfers")
                        print("5. Received Money")
                        print("6. Back")


                        filter_choice = input(
                            "\nEnter your choice: "
                        )


                        if filter_choice == "1":

                            print_account_statement(
                                user_account,
                                name,
                                accounts[
                                    user_account
                                ]["transactions"],
                                accounts[
                                    user_account
                                ]["balance"]
                            )


                        elif filter_choice == "2":

                            filter_transactions(
                                accounts[
                                    user_account
                                ]["transactions"],
                                "DEPOSIT"
                            )


                        elif filter_choice == "3":

                            filter_transactions(
                                accounts[
                                    user_account
                                ]["transactions"],
                                "WITHDRAW"
                            )


                        elif filter_choice == "4":

                            filter_transactions(
                                accounts[
                                    user_account
                                ]["transactions"],
                                "TRANSFER"
                            )


                        elif filter_choice == "5":

                            filter_transactions(
                                accounts[
                                    user_account
                                ]["transactions"],
                                "RECEIVED"
                            )


                        elif filter_choice == "6":

                            break


                        else:

                            print("\nInvalid choice.")

                            print(
                                "Please select a number "
                                "from 1 to 6."
                            )


                # ==========================================
                # EXPORT STATEMENT
                # ==========================================

                elif choice == "6":

                    export_statement_csv(
                        user_account,
                        name,
                        accounts[
                            user_account
                        ]["transactions"],
                        accounts[
                            user_account
                        ]["balance"]
                    )


                # ==========================================
                # CHANGE PIN
                # ==========================================

                elif choice == "7":

                    print(
                        "\n========== CHANGE PIN =========="
                    )


                    old_pin = getpass(
                        "Enter your current PIN: "
                    )


                    old_pin_hash = hashlib.sha256(
                        old_pin.encode()
                    ).hexdigest()


                    current_pin = accounts[
                        user_account
                    ]["pin"]


                    if old_pin_hash == current_pin:

                        new_pin = getpass(
                            "Enter your new PIN: "
                        )


                        confirm_pin = getpass(
                            "Confirm your new PIN: "
                        )


                        if new_pin != confirm_pin:

                            print(
                                "\nNew PINs do not match."
                            )


                        elif (
                            len(new_pin) != 4
                            or not new_pin.isdigit()
                        ):

                            print(
                                "\nPIN must contain "
                                "exactly 4 digits."
                            )


                        elif new_pin == old_pin:

                            print(
                                "\nNew PIN cannot be "
                                "the same as old PIN."
                            )


                        else:

                            new_pin_hash = (
                                hashlib.sha256(
                                    new_pin.encode()
                                ).hexdigest()
                            )


                            accounts[
                                user_account
                            ]["pin"] = new_pin_hash


                            save_accounts(accounts)


                            print(
                                "\nPIN changed successfully!"
                            )


                    else:

                        print(
                            "\nIncorrect current PIN."
                        )


                # ==========================================
                # LOGOUT
                # ==========================================

                elif choice == "8":

                    print(
                        "\nThank you for using "
                        "ATM Banking System."
                    )

                    print(
                        "Please take your card."
                    )

                    break


                # ==========================================
                # INVALID CHOICE
                # ==========================================

                else:

                    print("\nInvalid choice.")

                    print(
                        "Please select a number "
                        "from 1 to 8."
                    )


            # Return to login screen after logout
            break


        # ==========================================
        # WRONG PIN
        # ==========================================

        else:

            account["failed_attempts"] += 1

            remaining = (
                MAX_LOGIN_ATTEMPTS
                - account["failed_attempts"]
            )


            if remaining > 0:

                print(
                    "\nIncorrect PIN."
                )

                print(
                    "Attempts remaining:",
                    remaining
                )

                save_accounts(accounts)


            else:

                account["lock_until"] = (
                    time.time() + LOCK_TIME
                )

                account["failed_attempts"] = (
                    MAX_LOGIN_ATTEMPTS
                )

                save_accounts(accounts)


                print(
                    "\n========================================"
                )

                print(
                    "          ACCOUNT LOCKED"
                )

                print(
                    "========================================"
                )

                print(
                    "Too many incorrect PIN attempts."
                )

                print(
                    "Account locked for",
                    LOCK_TIME,
                    "seconds."
                )

                print(
                    "========================================"
                )

                break