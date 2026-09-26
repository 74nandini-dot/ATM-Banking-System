import os
import csv


# ==========================================
# FORMAT TRANSACTION
# ==========================================

def format_transaction(transaction):

    transaction_id = transaction.get(
        "transaction_id",
        "N/A"
    )

    date_time = transaction["date_time"]
    transaction_type = transaction["type"]
    amount = transaction["amount"]
    balance = transaction["balance"]
    details = transaction["details"]

    print("----------------------------------------")

    print(
        "Transaction ID :",
        transaction_id
    )

    print(
        "Date & Time    :",
        date_time
    )

    print(
        "Type           :",
        transaction_type
    )

    print(
        "Amount         : ₹",
        amount
    )

    if details:

        print(
            "Details        :",
            details
        )

    print(
        "Balance        : ₹",
        balance
    )

    print("----------------------------------------")


# ==========================================
# PRINT RECEIPT
# ==========================================

def print_receipt(
    account_number,
    account_name,
    transaction
):

    print("\n")

    print("========================================")
    print("          ATM TRANSACTION RECEIPT")
    print("========================================")

    print(
        "Account Holder :",
        account_name
    )

    print(
        "Account Number :",
        account_number
    )

    print(
        "Transaction ID :",
        transaction.get(
            "transaction_id",
            "N/A"
        )
    )

    print(
        "Transaction    :",
        transaction["type"]
    )

    print(
        "Amount         : ₹",
        transaction["amount"]
    )

    print(
        "Date & Time    :",
        transaction["date_time"]
    )

    if transaction["details"]:

        print(
            "Details        :",
            transaction["details"]
        )

    print(
        "Available Balance : ₹",
        transaction["balance"]
    )

    print("========================================")
    print("             THANK YOU")
    print("========================================")


# ==========================================
# SAVE RECEIPT
# ==========================================

def save_receipt(
    account_number,
    account_name,
    transaction
):

    receipt_folder = "receipts"

    if not os.path.exists(receipt_folder):

        os.makedirs(receipt_folder)

    date_time = transaction["date_time"]

    safe_date_time = date_time.replace(
        " ",
        "_"
    ).replace(
        ":",
        "-"
    )

    transaction_id = transaction.get(
        "transaction_id",
        "N/A"
    )

    file_name = (
        f"receipt_{account_number}_"
        f"{safe_date_time}_"
        f"{transaction_id}.txt"
    )

    file_path = os.path.join(
        receipt_folder,
        file_name
    )

    with open(
        file_path,
        "w"
    ) as file:

        file.write(
            "========================================\n"
        )

        file.write(
            "          ATM TRANSACTION RECEIPT\n"
        )

        file.write(
            "========================================\n"
        )

        file.write(
            f"Account Holder : {account_name}\n"
        )

        file.write(
            f"Account Number : {account_number}\n"
        )

        file.write(
            f"Transaction ID : {transaction_id}\n"
        )

        file.write(
            f"Transaction    : {transaction['type']}\n"
        )

        file.write(
            f"Amount         : ₹ {transaction['amount']}\n"
        )

        file.write(
            f"Date & Time    : {transaction['date_time']}\n"
        )

        if transaction["details"]:

            file.write(
                f"Details        : "
                f"{transaction['details']}\n"
            )

        file.write(
            f"Available Balance : "
            f"₹ {transaction['balance']}\n"
        )

        file.write(
            "========================================\n"
        )

        file.write(
            "             THANK YOU\n"
        )

        file.write(
            "========================================\n"
        )

    print("\nReceipt saved successfully!")

    print(
        "Receipt file:",
        file_path
    )


# ==========================================
# ACCOUNT STATEMENT
# ==========================================

def print_account_statement(
    account_number,
    account_name,
    transactions,
    balance
):

    print("\n")

    print("========================================")
    print("           ACCOUNT STATEMENT")
    print("========================================")

    print(
        "Account Holder :",
        account_name
    )

    print(
        "Account Number :",
        account_number
    )

    print(
        "\nTransaction ID       Date & Time"
    )

    print("----------------------------------------")

    if len(transactions) == 0:

        print("No transactions available.")

    else:

        for transaction in transactions:

            if isinstance(transaction, dict):

                print(
                    transaction.get(
                        "transaction_id",
                        "N/A"
                    )
                )

                print(
                    "Date & Time :",
                    transaction["date_time"]
                )

                print(
                    "Type        :",
                    transaction["type"]
                )

                print(
                    "Amount      : ₹",
                    transaction["amount"]
                )

                print("----------------------------------------")

    print(
        "Current Balance : ₹",
        balance
    )

    print(
        "Total Transactions :",
        len(transactions)
    )

    print("========================================")


# ==========================================
# FILTER TRANSACTIONS
# ==========================================

def filter_transactions(
    transactions,
    transaction_type
):

    print("\n========================================")
    print("         FILTERED TRANSACTIONS")
    print("========================================")

    found = False

    for transaction in transactions:

        if not isinstance(transaction, dict):

            continue

        if (
            transaction_type == "ALL"
            or transaction["type"] == transaction_type
        ):

            found = True

            print(
                "Transaction ID :",
                transaction.get(
                    "transaction_id",
                    "N/A"
                )
            )

            print(
                "Date & Time    :",
                transaction["date_time"]
            )

            print(
                "Type           :",
                transaction["type"]
            )

            print(
                "Amount         : ₹",
                transaction["amount"]
            )

            if transaction["details"]:

                print(
                    "Details        :",
                    transaction["details"]
                )

            print(
                "Balance        : ₹",
                transaction["balance"]
            )

            print("----------------------------------------")

    if not found:

        print(
            "No matching transactions found."
        )

    print("========================================")


# ==========================================
# EXPORT STATEMENT CSV
# ==========================================

def export_statement_csv(
    account_number,
    account_name,
    transactions,
    balance
):

    statement_folder = "statements"

    if not os.path.exists(statement_folder):

        os.makedirs(statement_folder)

    file_name = (
        f"statement_{account_number}.csv"
    )

    file_path = os.path.join(
        statement_folder,
        file_name
    )

    with open(
        file_path,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Account Holder",
                account_name
            ]
        )

        writer.writerow(
            [
                "Account Number",
                account_number
            ]
        )

        writer.writerow([])

        writer.writerow(
            [
                "Transaction ID",
                "Date & Time",
                "Transaction Type",
                "Amount",
                "Balance",
                "Details"
            ]
        )

        for transaction in transactions:

            if isinstance(transaction, dict):

                writer.writerow(
                    [
                        transaction.get(
                            "transaction_id",
                            "N/A"
                        ),
                        transaction["date_time"],
                        transaction["type"],
                        transaction["amount"],
                        transaction["balance"],
                        transaction["details"]
                    ]
                )

        writer.writerow([])

        writer.writerow(
            [
                "Current Balance",
                balance
            ]
        )

    print("\n========================================")
    print("   STATEMENT EXPORTED SUCCESSFULLY")
    print("========================================")

    print(
        "File:",
        file_path
    )

    print("========================================")