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
    posting_date: datetime
    direction: str

import xml.etree.ElementTree as ET
from models import Transaction


NAMESPACE = {
    "ns": "http://bpc.ru/sv/SVXP/clearing"
}


class VisaTransactionParser:

    def __init__(self, xml_path):
        self.xml_path = xml_path

    def parse(self):

        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        transactions = []

        operations = root.findall("ns:operation", NAMESPACE)

        for operation in operations:

            merchant_number = self.safe_text(
                operation,
                "ns:merchant_number"
            )

            mcc = self.safe_text(
                operation,
                "ns:mcc"
            )

            issuer = operation.find(
                "ns:issuer",
                NAMESPACE
            )

            customer_number = ""
            card_number = ""
            account_number = ""

            if issuer is not None:
                customer_number = self.safe_text(
                    issuer,
                    "ns:customer_number"
                )

                card_number = self.safe_text(
                    issuer,
                    "ns:card_number"
                )

                account_number = self.safe_text(
                    issuer,
                    "ns:account_number"
                )

            txns = operation.findall(
                "ns:transaction",
                NAMESPACE
            )

            for txn in txns:

                txn_id = self.safe_text(
                    txn,
                    "ns:transaction_id"
                )

                txn_type = self.safe_text(
                    txn,
                    "ns:transaction_type"
                )

                posting_date = self.safe_text(
                    txn,
                    "ns:posting_date"
                )

                debit_entry = txn.find(
                    "ns:debit_entry",
                    NAMESPACE
                )

                credit_entry = txn.find(
                    "ns:credit_entry",
                    NAMESPACE
                )

                direction = None
                amount = None
                currency = None

                if debit_entry is not None:
                    direction = "DEBIT"

                    amount = self.safe_text(
                        debit_entry,
                        "ns:amount/ns:amount_value"
                    )

                    currency = self.safe_text(
                        debit_entry,
                        "ns:amount/ns:currency"
                    )

                elif credit_entry is not None:
                    direction = "CREDIT"

                    amount = self.safe_text(
                        credit_entry,
                        "ns:amount/ns:amount_value"
                    )

                    currency = self.safe_text(
                        credit_entry,
                        "ns:amount/ns:currency"
                    )

                transaction = Transaction(
                    transaction_id=txn_id,
                    customer_number=customer_number,
                    card_number=card_number,
                    account_number=account_number,
                    merchant_number=merchant_number,
                    mcc=mcc,
                    transaction_type=txn_type,
                    amount=float(amount) / 100,
                    currency=currency,
                    posting_date=posting_date,
                    direction=direction
                )

                transactions.append(transaction)

        return transactions

    def safe_text(self, node, xpath):

        if node is None:
            return ""

        item = node.find(xpath, NAMESPACE)

        if item is None:
            return ""

        return item.text or ""

parser = VisaTransactionParser(
    "KCASH_CREDIT_TRANS_18022024120000962214.xml"
)

transactions = parser.parse()

print(f"Loaded {len(transactions)} transactions")

for tx in transactions[:5]:
    print(tx)
    import pandas as pd

df = pd.DataFrame(
    [vars(t) for t in transactions]
)

print(df.head())