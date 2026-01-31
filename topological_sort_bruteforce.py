from dataclasses import dataclass
from typing import List


@dataclass
class Section:
    id: str
    order: int
    dependsOn: List[str]


def resolve_dependency_order(sections: List[Section]) -> List[Section]:
    """Return sorted sections based on their dependencies or natural order."""

    # First lets sort all sections by their natural order
    sortedByOrder = sorted(sections, key=lambda s: s.order)

    stack = []  # This will hold the final ordered list

    # Looping over all sections until they all are processed
    while sortedByOrder:

        circulation_detected = True

        for section in sortedByOrder:
            addSection = True

            # Before adding section, lets do quick dependency check
            for depends_id in section.dependsOn:
                if depends_id not in [s.id for s in stack]:
                    addSection = False  # Skip Section if dependency missing
                    break

            if addSection:
                stack.append(section)  # Add section to final stack
                sortedByOrder.remove(section)  # Remove processed section
                circulation_detected = False
                break

        if circulation_detected:
            raise ValueError("Circular dependency detected")

    return stack


if __name__ == "__main__":
    sections = [
        Section("base", 0, []),
        Section("left", 1, ["base"]),
        Section("right", 2, ["base"]),
        Section("top", 3, ["left", "right"]),
    ]
    result = resolve_dependency_order(sections)
    print([s.id for s in result])
