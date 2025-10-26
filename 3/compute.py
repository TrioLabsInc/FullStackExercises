INVOICES = [
    {
        "id": "INV-100",
        "expected_total": 100.0,
        "transactions": [20.0, 30.0, 50.0],
    },
    {
        "id": "INV-101",
        "expected_total": 42.5,
        "transactions": [10.0, 10.0, 10.0, 12.5],
    },
    {
        "id": "INV-102",
        "expected_total": 5.0,
        "transactions": [0.1] * 50,
    },
]


def invoice_balances_match(invoice: dict) -> bool:
    total = 0.0
    for value in invoice["transactions"]:
        total += value
    return total == invoice["expected_total"]


def main() -> None:
    for invoice in INVOICES:
        if not invoice_balances_match(invoice):
            print(f"{invoice['id']} is off!")
    print("done")


if __name__ == "__main__":
    main()
