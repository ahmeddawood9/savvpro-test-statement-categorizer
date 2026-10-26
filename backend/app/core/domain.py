from typing import Literal, get_args

Category = Literal[
    "Software & Subscriptions",
    "Hosting & Cloud",
    "Hardware & Equipment",
    "Internet & Phone",
    "Travel",
    "Meals",
    "Office Supplies",
    "Professional Services",
    "Bank Fees",
    "Income",
    "Transfer",
    "Refund",
    "Personal",
    "Tax Withheld",
    "Needs Review",
]
Kind = Literal["expense", "income", "transfer", "refund", "fee", "tax"]
Direction = Literal["in", "out"]  # money in / money out
AccountType = Literal["card", "bank"]

CATEGORIES: tuple[str, ...] = get_args(Category)
KINDS: tuple[str, ...] = get_args(Kind)
NEEDS_REVIEW: Category = "Needs Review"
