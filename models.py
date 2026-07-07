from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    transaction_id: str
    customer_number: str
    card_number: str
    account_number: str
    merchant_number: str
    mcc: str
    transaction_type: str
    amount: float
    currency: str
    posting_date: str
    direction: str