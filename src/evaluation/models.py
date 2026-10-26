"""
Data models for evaluation experiments.
"""

from dataclasses import dataclass, field


@dataclass
class Entity:
    """Represents an annotated PII entity in text."""

    start: int
    end: int
    entity_type: str  # email, phone, ssn, etc.
    text: str
    confidence: float = 1.0


@dataclass
class GroundTruthAnnotation:
    """Ground truth annotation for a single text sample."""

    text: str
    entities: list[Entity] = field(default_factory=list)
    source: str = "synthetic"  # synthetic, manual, hybrid
    metadata: dict[str, any] = field(default_factory=dict)

    def add_entity(self, entity: Entity) -> None:
        """Add an entity annotation."""
        self.entities.append(entity)

    @property
    def has_pii(self) -> bool:
        """Check if text contains PII."""
        return len(self.entities) > 0

    @property
    def entity_types(self) -> set[str]:
        """Get unique entity types."""
        return {e.entity_type for e in self.entities}


@dataclass
class SyntheticDatasetConfig:
    """Configuration for synthetic dataset generation."""

    size: int = 100  # Number of samples
    seed: int = 42  # Random seed for reproducibility
    positive_ratio: float = 0.7  # Ratio of samples with PII

    # PII type distribution (sum should be ~1.0)
    email_prob: float = 0.3
    phone_prob: float = 0.25
    ssn_prob: float = 0.15
    credit_card_prob: float = 0.10
    date_prob: float = 0.10
    ip_address_prob: float = 0.10

    # Text generation
    min_length: int = 50  # Minimum text length
    max_length: int = 200  # Maximum text length
    include_noise: bool = True  # Add non-PII noise text
