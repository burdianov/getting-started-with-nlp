information = "When Sally met Harry"

words = information.split()

print(f"Participant 1 = {words[words.index('met')-1]}")
print(f"Action = met")
print(f"Participant 2 = {words[words.index('met')+1]}")
