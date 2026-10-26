"""
Tests for synthetic dataset generation.
"""


from src.evaluation import generate_synthetic_dataset
from src.evaluation.models import (
    Entity,
    GroundTruthAnnotation,
    SyntheticDatasetConfig,
)


class TestGenerateSyntheticDataset:
    """Tests for generate_synthetic_dataset function."""

    def test_generate_default_config(self):
        """Test generation with default config."""
        annotations = generate_synthetic_dataset()

        assert len(annotations) == 100  # Default size
        assert all(isinstance(a, GroundTruthAnnotation) for a in annotations)

    def test_custom_size(self):
        """Test custom dataset size."""
        config = SyntheticDatasetConfig(size=50)
        annotations = generate_synthetic_dataset(config)

        assert len(annotations) == 50

    def test_positive_ratio(self):
        """Test positive ratio control."""
        config = SyntheticDatasetConfig(size=100, positive_ratio=0.5)
        annotations = generate_synthetic_dataset(config)

        positive_count = sum(1 for a in annotations if a.has_pii)
        # Allow some variation due to randomness in PII type selection
        assert 40 <= positive_count <= 60

    def test_all_positive_samples(self):
        """Test generating all positive samples."""
        config = SyntheticDatasetConfig(size=20, positive_ratio=1.0)
        annotations = generate_synthetic_dataset(config)

        positive_count = sum(1 for a in annotations if a.has_pii)
        assert positive_count == 20

    def test_all_negative_samples(self):
        """Test generating all negative samples."""
        config = SyntheticDatasetConfig(size=20, positive_ratio=0.0)
        annotations = generate_synthetic_dataset(config)

        negative_count = sum(1 for a in annotations if not a.has_pii)
        assert negative_count == 20

    def test_reproducibility_with_seed(self):
        """Test reproducibility with same seed."""
        config1 = SyntheticDatasetConfig(size=10, seed=42)
        config2 = SyntheticDatasetConfig(size=10, seed=42)

        annotations1 = generate_synthetic_dataset(config1)
        annotations2 = generate_synthetic_dataset(config2)

        # Same seed should produce same text
        for a1, a2 in zip(annotations1, annotations2, strict=False):
            assert a1.text == a2.text
            assert len(a1.entities) == len(a2.entities)

    def test_different_seeds_produce_different_data(self):
        """Test different seeds produce different data."""
        config1 = SyntheticDatasetConfig(size=10, seed=42)
        config2 = SyntheticDatasetConfig(size=10, seed=123)

        annotations1 = generate_synthetic_dataset(config1)
        annotations2 = generate_synthetic_dataset(config2)

        # Different seeds should produce different text
        different_count = sum(
            1 for a1, a2 in zip(annotations1, annotations2, strict=False) if a1.text != a2.text
        )
        assert different_count > 5  # Most should be different

    def test_entity_annotations_valid(self):
        """Test entity annotations are valid."""
        config = SyntheticDatasetConfig(size=20, positive_ratio=1.0)
        annotations = generate_synthetic_dataset(config)

        for annotation in annotations:
            for entity in annotation.entities:
                # Entity positions should be valid
                assert 0 <= entity.start < entity.end <= len(annotation.text)
                # Entity text should match the slice
                assert annotation.text[entity.start : entity.end] == entity.text
                # Entity type should be uppercase
                assert entity.entity_type.isupper()

    def test_pii_type_distribution(self):
        """Test various PII types are generated."""
        config = SyntheticDatasetConfig(size=100, positive_ratio=1.0)
        annotations = generate_synthetic_dataset(config)

        all_types = set()
        for annotation in annotations:
            all_types.update(annotation.entity_types)

        # Should have multiple PII types
        assert len(all_types) >= 3

    def test_text_length_within_bounds(self):
        """Test text length is within configured bounds."""
        config = SyntheticDatasetConfig(
            size=20, min_length=50, max_length=200, positive_ratio=0.0
        )
        annotations = generate_synthetic_dataset(config)

        for annotation in annotations:
            # Negative samples should respect length
            if not annotation.has_pii:
                assert 40 <= len(annotation.text) <= 250  # Allow some variance

    def test_metadata_populated(self):
        """Test metadata is populated."""
        annotations = generate_synthetic_dataset()

        for annotation in annotations:
            assert "pii_types" in annotation.metadata
            assert isinstance(annotation.metadata["pii_types"], list)


class TestGroundTruthAnnotation:
    """Tests for GroundTruthAnnotation model."""

    def test_create_annotation(self):
        """Test creating annotation."""
        annotation = GroundTruthAnnotation(text="Test text")

        assert annotation.text == "Test text"
        assert len(annotation.entities) == 0
        assert annotation.source == "synthetic"

    def test_add_entity(self):
        """Test adding entity."""
        annotation = GroundTruthAnnotation(text="Email: test@example.com")
        entity = Entity(start=7, end=23, entity_type="EMAIL", text="test@example.com")

        annotation.add_entity(entity)

        assert len(annotation.entities) == 1
        assert annotation.entities[0].text == "test@example.com"

    def test_has_pii_property(self):
        """Test has_pii property."""
        annotation = GroundTruthAnnotation(text="Test")
        assert not annotation.has_pii

        annotation.add_entity(
            Entity(start=0, end=4, entity_type="TEST", text="Test")
        )
        assert annotation.has_pii

    def test_entity_types_property(self):
        """Test entity_types property."""
        annotation = GroundTruthAnnotation(text="Test")
        annotation.add_entity(
            Entity(start=0, end=4, entity_type="EMAIL", text="test")
        )
        annotation.add_entity(
            Entity(start=0, end=4, entity_type="PHONE", text="test")
        )

        types = annotation.entity_types
        assert len(types) == 2
        assert "EMAIL" in types
        assert "PHONE" in types


class TestEntity:
    """Tests for Entity model."""

    def test_create_entity(self):
        """Test creating entity."""
        entity = Entity(
            start=0, end=10, entity_type="EMAIL", text="test@email.com", confidence=0.95
        )

        assert entity.start == 0
        assert entity.end == 10
        assert entity.entity_type == "EMAIL"
        assert entity.text == "test@email.com"
        assert entity.confidence == 0.95

    def test_default_confidence(self):
        """Test default confidence value."""
        entity = Entity(start=0, end=5, entity_type="TEST", text="test")

        assert entity.confidence == 1.0


class TestSyntheticDatasetConfig:
    """Tests for SyntheticDatasetConfig model."""

    def test_default_config(self):
        """Test default configuration."""
        config = SyntheticDatasetConfig()

        assert config.size == 100
        assert config.seed == 42
        assert config.positive_ratio == 0.7

    def test_custom_config(self):
        """Test custom configuration."""
        config = SyntheticDatasetConfig(
            size=50, seed=123, positive_ratio=0.5, email_prob=0.5
        )

        assert config.size == 50
        assert config.seed == 123
        assert config.positive_ratio == 0.5
        assert config.email_prob == 0.5
