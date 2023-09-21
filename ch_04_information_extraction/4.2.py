meetings = [
    ("Boris Johnson", "meets with", "the Queen"),
    ("Donald Trump", "meets with", "his cabinet"),
    ("administration", "meets with", "tech giants"),
    ("the Queen", "meets with", "the Prime Minister"),
    ("Donald Trump", "meets with", "Finnish President"),
]

query = [p2 for (p1, act, p2) in meetings if p1 == "the Queen"]
query += [p1 for (p1, act, p2) in meetings if p2 == "the Queen"]

print(query)
