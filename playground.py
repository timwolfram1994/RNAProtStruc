sets = [{frozenset({'H', 'D'}), frozenset({'B', 'A'}),
         frozenset({'F', 'I'})},  # 5 (enhält 1)
        {frozenset({'B', 'D'}), frozenset({'E', 'F'}),frozenset({'Y','Z'})},  # 3
        {frozenset({'D', 'H'}), frozenset({'B', 'A'}), frozenset({'I', 'F'}),
         frozenset({'F', 'E'})}]
a = frozenset({'E', 'F'})
for edge in sets[1]:
    if a in sets[2]:
        print("a found")
        break
sets[2].update(sets[1])
print(sets[2])