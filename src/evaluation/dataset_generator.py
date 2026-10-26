"""
Synthetic dataset generation for evaluation experiments.
"""

import logging
import random

from faker import Faker

from src.evaluation.models import (
    Entity,
    GroundTruthAnnotation,
    SyntheticDatasetConfig,
)

logger = logging.getLogger(__name__)


def generate_synthetic_dataset(
    config: SyntheticDatasetConfig | None = None,
) -> list[GroundTruthAnnotation]:
    """
    Generate synthetic dataset with ground truth annotations.

    Args:
        config: Dataset configuration (default if None)

    Returns:
        List of annotated text samples
    """
    if config is None:
        config = SyntheticDatasetConfig()

    random.seed(config.seed)
    fake = Faker()
    Faker.seed(config.seed)

    logger.info(f"Generating {config.size} synthetic samples...")

    annotations = []

    # Calculate number of positive and negative samples
    positive_count = int(config.size * config.positive_ratio)
    negative_count = config.size - positive_count

    # Generate positive samples (with PII)
    for _i in range(positive_count):
        annotation = _generate_positive_sample(fake, config)
        annotations.append(annotation)

    # Generate negative samples (without PII)
    for _i in range(negative_count):
        annotation = _generate_negative_sample(fake, config)
        annotations.append(annotation)

    # Shuffle
    random.shuffle(annotations)

    logger.info(
        f"Generated {len(annotations)} samples "
        f"({positive_count} positive, {negative_count} negative)"
    )

    return annotations


def _generate_positive_sample(
    fake: Faker, config: SyntheticDatasetConfig
) -> GroundTruthAnnotation:
    """Generate a sample with PII."""
    # Decide which PII types to include
    pii_types = []
    if random.random() < config.email_prob:
        pii_types.append("email")
    if random.random() < config.phone_prob:
        pii_types.append("phone")
    if random.random() < config.ssn_prob:
        pii_types.append("ssn")
    if random.random() < config.credit_card_prob:
        pii_types.append("credit_card")
    if random.random() < config.date_prob:
        pii_types.append("date")
    if random.random() < config.ip_address_prob:
        pii_types.append("ip_address")

    # Ensure at least one PII type
    if not pii_types:
        pii_types = [random.choice(["email", "phone", "ssn"])]

    # Build text with PII
    text_parts = []
    entities = []
    current_pos = 0

    # Add optional intro noise
    if config.include_noise and random.random() < 0.5:
        intro = fake.sentence()
        text_parts.append(intro)
        current_pos += len(intro) + 1  # +1 for space

    # Add PII entities
    for pii_type in pii_types:
        # Add connector text
        if config.include_noise:
            connector = _get_connector_text(fake, pii_type)
            text_parts.append(connector)
            current_pos += len(connector) + 1

        # Add PII
        pii_text = _generate_pii_value(fake, pii_type)
        text_parts.append(pii_text)

        entity = Entity(
            start=current_pos,
            end=current_pos + len(pii_text),
            entity_type=pii_type.upper(),
            text=pii_text,
            confidence=1.0,
        )
        entities.append(entity)

        current_pos += len(pii_text) + 1

    # Add optional closing noise
    if config.include_noise and random.random() < 0.5:
        closing = fake.sentence()
        text_parts.append(closing)

    text = " ".join(text_parts)

    annotation = GroundTruthAnnotation(
        text=text,
        entities=entities,
        source="synthetic",
        metadata={"pii_types": pii_types},
    )

    return annotation


def _generate_negative_sample(
    fake: Faker, config: SyntheticDatasetConfig
) -> GroundTruthAnnotation:
    """Generate a sample without PII."""
    # Generate random text without PII
    sentences = []
    target_length = random.randint(config.min_length, config.max_length)

    while sum(len(s) for s in sentences) < target_length:
        sentences.append(fake.sentence())

    text = " ".join(sentences)

    annotation = GroundTruthAnnotation(
        text=text,
        entities=[],
        source="synthetic",
        metadata={"pii_types": []},
    )

    return annotation


def _generate_pii_value(fake: Faker, pii_type: str) -> str:
    """Generate a PII value of specified type."""
    if pii_type == "email":
        return fake.email()
    elif pii_type == "phone":
        # Use various phone formats
        formats = [
            fake.phone_number(),
            f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            f"({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
        ]
        return random.choice(formats)
    elif pii_type == "ssn":
        return fake.ssn()
    elif pii_type == "credit_card":
        return fake.credit_card_number()
    elif pii_type == "date":
        # Generate various date formats
        date = fake.date_of_birth(minimum_age=18, maximum_age=90)
        formats = [
            date.strftime("%Y-%m-%d"),
            date.strftime("%m/%d/%Y"),
            date.strftime("%B %d, %Y"),
        ]
        return random.choice(formats)
    elif pii_type == "ip_address":
        return fake.ipv4()
    else:
        return fake.word()


def _get_connector_text(fake: Faker, pii_type: str) -> str:
    """Get connector text for a PII type."""
    connectors = {
        "email": [
            "My email is",
            "Contact me at",
            "Email:",
            "Send to",
            "You can reach me at",
        ],
        "phone": [
            "Call me at",
            "Phone:",
            "My number is",
            "Reach me at",
            "Contact:",
        ],
        "ssn": [
            "SSN:",
            "Social Security Number:",
            "My SSN is",
            "ID:",
        ],
        "credit_card": [
            "Card number:",
            "Credit card:",
            "Payment card:",
            "CC:",
        ],
        "date": [
            "Born on",
            "Date of birth:",
            "DOB:",
            "Birthday:",
        ],
        "ip_address": [
            "IP address:",
            "Server at",
            "Host:",
            "Connect to",
        ],
    }

    return random.choice(connectors.get(pii_type, ["Information:"]))


def save_dataset_to_file(
    annotations: list[GroundTruthAnnotation], output_path: str
) -> None:
    """
    Save dataset to JSON file.

    Args:
        annotations: List of annotations
        output_path: Output file path
    """
    import json

    data = []
    for annotation in annotations:
        data.append(
            {
                "text": annotation.text,
                "entities": [
                    {
                        "start": e.start,
                        "end": e.end,
                        "entity_type": e.entity_type,
                        "text": e.text,
                        "confidence": e.confidence,
                    }
                    for e in annotation.entities
                ],
                "source": annotation.source,
                "metadata": annotation.metadata,
            }
        )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved {len(annotations)} annotations to {output_path}")


def load_dataset_from_file(input_path: str) -> list[GroundTruthAnnotation]:
    """
    Load dataset from JSON file.

    Args:
        input_path: Input file path

    Returns:
        List of annotations
    """
    import json

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    annotations = []
    for item in data:
        entities = [
            Entity(
                start=e["start"],
                end=e["end"],
                entity_type=e["entity_type"],
                text=e["text"],
                confidence=e.get("confidence", 1.0),
            )
            for e in item["entities"]
        ]

        annotation = GroundTruthAnnotation(
            text=item["text"],
            entities=entities,
            source=item.get("source", "unknown"),
            metadata=item.get("metadata", {}),
        )
        annotations.append(annotation)

    logger.info(f"Loaded {len(annotations)} annotations from {input_path}")
    return annotations
