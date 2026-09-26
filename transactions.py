from datetime import datetime
import random


def create_transaction(
    transaction_type,
    amount,
    balance,
    details=""
):

    date_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    random_number = random.randint(
        1000,
        9999
    )

    transaction_id = (
        f"TXN-{timestamp}-{random_number}"
    )

    transaction = {

        "transaction_id": transaction_id,

        "date_time": date_time,

        "type": transaction_type,

        "amount": amount,

        "balance": balance,

        "details": details
    }

    return transaction