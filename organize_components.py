components = [{frozenset({'H', 'I'})}, {frozenset({'J', 'I'})},
              {frozenset({'H', 'I'}), frozenset({'J', 'I'}), frozenset({'H', 'J'})}, {frozenset({'H', 'G'})},
              {frozenset({'G', 'F'})}, {frozenset({'E', 'F'})}, {frozenset({'D', 'G'})},
              {frozenset({'G', 'F'}), frozenset({'D', 'F'}), frozenset({'D', 'G'})},
              {frozenset({'E', 'G'}), frozenset({'E', 'F'}), frozenset({'D', 'F'}), frozenset({'D', 'G'}),
               frozenset({'E', 'D'}), frozenset({'G', 'F'})}, {frozenset({'J', 'C'})}, {frozenset({'C', 'D'})},
              {frozenset({'D', 'B'})}, {frozenset({'D', 'B'}), frozenset({'C', 'D'}), frozenset({'C', 'B'})},
              {frozenset({'A', 'C'})},
              {frozenset({'A', 'B'}), frozenset({'D', 'B'}), frozenset({'C', 'D'}), frozenset({'A', 'C'}),
               frozenset({'A', 'D'}), frozenset({'C', 'B'})}]
components_to_remove = []

# Iterate through the components and mark isolated components for removal
for i in range(len(components)):
    if len(components[i]) == 1:
        components_to_remove.append(i)

# Iterate through the components to merge connected components
for i in range(len(components) - 1, -1, -1):
    if i in components_to_remove:
        continue

    for j in range(i - 1, -1, -1):
        if j in components_to_remove:
            continue

        for edge in components[i]:
            if edge in components[j]:
                components[j].update(components[i])
                components_to_remove.append(i)
                break

# Remove the marked components
for i in sorted(components_to_remove, reverse=True):
    components.pop(i)

# Print the modified components
for component in components:
    print(component)
