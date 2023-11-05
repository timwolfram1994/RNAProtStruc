import components_json.HIV_components


def organize_components(components: list):
    unwanted_components = []
    component_updated = False

    for i in range(len(components) - 1):
        component_updated = False
        if len(components[i]) == 1:
            continue
        else:
            for j in range(i + 1, len(components)):
                if len(components[j]) == 1:
                    continue
                for edge in components[i]:
                    if edge in components[j]:
                        # print("comp_i_before:", components[i])
                        # print("comp_j_before:", components[j])
                        components[j].update(components[i])
                        # print(components[j])
                        unwanted_components.append(components[i])
                        component_updated = True
                        break
                if component_updated is True:
                    break

    components_filtered = []
    for component in components:
        if len(component) > 1:
            if component in unwanted_components:
                unwanted_components.remove(component)
                continue

            components_filtered.append(component)

    return components_filtered


if __name__ == "__main__":
    sets = [{frozenset({'A', 'B'}), frozenset({'B', 'C'})},  # 1

            {frozenset({'B', 'C'})},  # 2

            {frozenset({'B', 'D'}), frozenset({'E', 'F'}), frozenset({'Y', 'Z'})},  # 3

            {frozenset({'F', 'G'})},  # 4

            {frozenset({'H', 'D'}), frozenset({'B', 'A'}),
             frozenset({'F', 'I'})},  # 5 (enhält 1)

            {frozenset({'D', 'H'}), frozenset({'B', 'A'}), frozenset({'I', 'F'}),
             frozenset({'F', 'E'})}

            ]

    sets2 = [{frozenset({'A', 'B'}), frozenset({'B', 'C'})},  # 1

             {frozenset({'B', 'C'})},  # 2

             {frozenset({'B', 'D'}), frozenset({'E', 'F'})},  # 3

             {frozenset({'F', 'G'}), frozenset({'B', 'F'})},  # 4

             {frozenset({'H', 'D'}), frozenset({'B', 'A'}),
              frozenset({'F', 'I'})},  # 5 (enhält 1)

             {frozenset({'D', 'H'}), frozenset({'B', 'A'}),
              frozenset({'I', 'F'}), frozenset({'F', 'E'})},

             {frozenset({'F', 'B'}), frozenset({'C', 'X'}),
              frozenset({'T', 'F'}), frozenset({'F', 'Q'})}]

    organized = organize_components(sets2)
    for component in organized:
        print(component)


