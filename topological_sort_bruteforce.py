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
                if depends_id not in stack:
                    addSection = False  # Skip Section if dependency missing
                    break

            if addSection:
                stack.append(section.id)  # Add section to final stack
                sortedByOrder.remove(section)  # Remove processed section
                circulation_detected = False
                break

        if circulation_detected:
            raise ValueError("Circular dependency detected")

    return stack


if __name__ == "__main__":
    sections = [
        Section("summary", 0, ["details"]),
        Section("details", 1, []),
        Section("intro", 2, []),
    ]
    result = resolve_dependency_order(sections)
    print(result)
