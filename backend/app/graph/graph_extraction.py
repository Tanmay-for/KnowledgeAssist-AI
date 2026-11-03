
import re

from backend.app.graph.knowledge_graph import (
    add_concept,
    add_relationship,
    save_graph,
    load_graph
)

ROOT_CONCEPT = "Object-Oriented Programming"

CONCEPTS = [
    ROOT_CONCEPT,
    "Class",
    "Object",
    "Encapsulation",
    "Inheritance",
    "Polymorphism",
    "Abstraction",
    "Constructor",
    "Destructor",
    "Function",
    "Data Member",
    "Member Function"
]

# Original sentence-based relationship rules.
RELATIONSHIP_RULES = [
    ("Object", "Class",
     r"\b(instance of|instantiated from|belongs to)\b",
     "instance_of"),

    ("Class", "Object",
     r"\b(creates|create|instantiates|instantiate|produces)\b",
     "creates"),

    ("Inheritance", "Class",
     r"\b(inherits|inheritance|derived class|base class|extends)\b",
     "supports"),

    ("Polymorphism", "Function",
     r"\b(overload\w*|overrid\w*|same function|multiple forms)\b",
     "supports"),

    ("Encapsulation", "Data Member",
     r"\b(protects|protect|hides|binding|data hiding)\b",
     "protects"),

    ("Abstraction", "Object",
     r"\b(hides|hide|complexity|implementation details)\b",
     "hides"),

    ("Constructor", "Class",
     r"\b(initializes|initialize|initialization|called when object)\b",
     "initializes"),

    ("Destructor", "Object",
     r"\b(destroys|destroy|cleanup|deallocated)\b",
     "destroys"),

    ("Member Function", "Class",
     r"\b(member function|method|belongs to|defined inside)\b",
     "belongs_to"),

    ("Data Member", "Class",
     r"\b(data member|member variable|attribute)\b",
     "belongs_to")
]

# Additional conceptual relationship rules.
INFERRED_RELATIONSHIP_RULES = [
    (
        "Encapsulation",
        "Data Member",
        r"\b(encapsulat\w*|data hiding|protect\w*|private|access specifiers|bind\w*)\b",
        "protects"
    ),
    (
        "Destructor",
        "Object",
        r"\b(destroy\w*|cleanup|clean up|deallocat\w*|end of lifetime|goes out of scope|automatically called)\b",
        "destroys"
    ),
    (
        "Abstraction",
        "Implementation Details",
        r"\b(hid\w*|implementation details|complexity|essential features|exposes only|interface)\b",
        "hides"
    )
]


def extract_concepts(text: str) -> list:
    if not text:
        return []

    found = []

    # Recognise different spellings of OOP.
    root_pattern = (
        r"\b(object[\s-]*oriented[\s-]*programming|O\.?O\.?P\.?)\b"
    )

    if re.search(root_pattern, text, re.IGNORECASE):
        found.append(ROOT_CONCEPT)

    # Extract other known concepts.
    for concept in CONCEPTS:
        if concept == ROOT_CONCEPT:
            continue

        pattern = r"\b" + re.escape(concept) + r"\b"

        if re.search(pattern, text, re.IGNORECASE):
            found.append(concept)

    return found


def extract_relationships(text: str) -> list:
    relationships = []
    seen = set()

    if not text:
        return relationships

    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        sentence_concepts = extract_concepts(sentence)

        # Original rules: both concepts must be present.
        for source, target, pattern, label in RELATIONSHIP_RULES:
            if (
                source in sentence_concepts
                and target in sentence_concepts
                and re.search(pattern, sentence, re.IGNORECASE)
            ):
                key = (source, target, label)

                if key not in seen:
                    relationships.append({
                        "source": source,
                        "target": target,
                        "relationship": label
                    })
                    seen.add(key)

        # Additional conceptual rules.
        for source, target, pattern, label in INFERRED_RELATIONSHIP_RULES:
            if (
                source in sentence_concepts
                and re.search(pattern, sentence, re.IGNORECASE)
            ):
                key = (source, target, label)

                if key not in seen:
                    relationships.append({
                        "source": source,
                        "target": target,
                        "relationship": label
                    })
                    seen.add(key)

    return relationships


def build_graph_from_text(text: str, document_id: str) -> dict:
    load_graph()

    concepts = extract_concepts(text)

    # No OOP concepts found: do not create an unrelated root.
    if not concepts:
        return {
            "concepts": [],
            "relationships": []
        }

    # Use OOP as the main root when this is an OOP document.
    if ROOT_CONCEPT not in concepts:
        concepts.append(ROOT_CONCEPT)

    # Add extracted concepts.
    for concept in concepts:
        add_concept(concept, document_id)

    # Connect every extracted OOP concept to the root.
    # These are deliberate subject-hierarchy links.
    root_relationships = []

    for concept in concepts:
        if concept == ROOT_CONCEPT:
            continue

        add_relationship(
            ROOT_CONCEPT,
            concept,
            "includes",
            document_id
        )

        root_relationships.append({
            "source": ROOT_CONCEPT,
            "target": concept,
            "relationship": "includes"
        })

    # Extract more specific relationships from sentences.
    relationships = extract_relationships(text)

    for item in relationships:
        source = item["source"]
        target = item["target"]
        label = item["relationship"]

        add_concept(source, document_id)
        add_concept(target, document_id)

        add_relationship(
            source,
            target,
            label,
            document_id
        )

    # Save the updated graph.
    save_graph()

    return {
        "concepts": concepts,
        "relationships": root_relationships + relationships
    }
