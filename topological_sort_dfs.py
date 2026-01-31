from dataclasses import dataclass
from typing import List


@dataclass
class Section:
    id: str
    order: int
    dependsOn: List[str]


def findTopoSort(
    sectionID: str, explorationDict: dict, sectionsDict: dict, stack: list
) -> None:
    """Performs a DFS algo to find the topological order."""

    if explorationDict[sectionID] == "Exploring":
        raise ValueError(f"Circular dependency detected")

    # Return if sectionID is already explored
    if explorationDict[sectionID] == "Explored":
        return

    # Exploring dependencies
    explorationDict[sectionID] = "Exploring"
    for depends_id in sectionsDict[sectionID].dependsOn:
        findTopoSort(depends_id, explorationDict, sectionsDict, stack)

    explorationDict[sectionID] = "Explored"
    stack.append(sectionsDict[sectionID])  # Add section ID to final stack


def resolve_dependency_order(sections: List[Section]) -> List[Section]:
    """Performs topological sort based on section's dependencies or order."""

    sortedByOrder = sorted(sections, key=lambda s: s.order)

    # Creating a dict of sectionID wrt their dependencies
    sectionsDict = {section.id: section for section in sections}

    # Dict to keep track of exploration status
    explorationDict = {section.id: "Not Explored yet" for section in sections}

    stack = []  # This Stack will hold our final ordered list

    # Loop over each section in sorted Sections
    for section in sortedByOrder:
        if explorationDict[section.id] == "Not Explored yet":
            findTopoSort(section.id, explorationDict, sectionsDict, stack)

    # Returning each section IDs as a List
    return stack


if __name__ == "__main__":
    sections = [
        Section("summary", 0, ["details"]),
        Section("details", 1, []),
        Section("intro", 2, []),
    ]
    result = resolve_dependency_order(sections)
    print([s.id for s in result])
