# Data and Research Specification
## Privacy-Aware Data Engineering Pipeline

**Version:** 1.0  
**Date:** October 25, 2026

---

## 1. Data Specifications

### 1.1 Input Data Formats

#### 1.1.1 CSV Format

**Structure:**
```csv
column1,column2,column3
value1,value2,value3
value4,value5,value6
```

**Requirements:**
- **Encoding**: UTF-8 (with fallback detection for other encodings)
- **Delimiter**: Comma (`,`) default, auto-detect or configurable
- **Quote character**: Double quote (`"`) for fields containing delimiters
- **Header row**: Required (first row contains column names)
- **Line endings**: CRLF (`\r\n`) or LF (`\n`)
- **Maximum file size**: 50 MB (configurable)
- **Maximum rows**: 100,000 (configurable)

**Validation:**
- All rows must have same number of columns as header
- Column names must be unique and non-empty
- No binary or executable content

**Example:**
```csv
customer_id,name,email,phone,address
1001,"John Doe",john.doe@example.com,(555) 123-4567,"123 Main St, City, ST 12345"
1002,"Jane Smith",jane.smith@example.com,(555) 987-6543,"456 Oak Ave, Town, ST 67890"
```

#### 1.1.2 JSON Format

**Structure Option 1: Array of Objects (Preferred)**
```json
[
  {
    "customer_id": 1001,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "(555) 123-4567"
  },
  {
    "customer_id": 1002,
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "(555) 987-6543"
  }
]
```

**Structure Option 2: Single Object (Supported)**
```json
{
  "records": [
    {"customer_id": 1001, "name": "John Doe", ...},
    {"customer_id": 1002, "name": "Jane Smith", ...}
  ]
}
```

**Requirements:**
- **Encoding**: UTF-8
- **Structure**: Array of flat objects (nested objects supported with flattening option)
- **Maximum file size**: 50 MB (configurable)
- **Maximum records**: 100,000 (configurable)

**Validation:**
- Valid JSON syntax
- Consistent schema across records (same keys)
- No executable content

**Flattening Example:**
```json
// Nested
{"user": {"name": "John", "email": "john@example.com"}}
// Flattened
{"user_name": "John", "user_email": "john@example.com"}
```

---

### 1.2 Data Quality Specifications

#### 1.2.1 Quality Issues to Detect

**Missing Values:**
- **Definition**: NULL, empty string, "N/A", "None", or whitespace-only values
- **Measurement**: Count and percentage per column
- **Severity**: Warning if >5%, Error if >20%

**Duplicate Rows:**
- **Definition**: Exact match across all columns, or key-based match
- **Measurement**: Count of duplicate rows
- **Severity**: Warning if any duplicates found

**Type Inconsistencies:**
- **Definition**: Mixed data types within a column (e.g., "123" and "abc" in numeric column)
- **Detection**: Infer expected type, flag deviations
- **Severity**: Warning

**Invalid Formats:**
- **Email**: Does not match basic email pattern (local@domain)
- **Phone**: Does not match expected phone patterns
- **Severity**: Warning

**Constraint Violations:**
- **Range**: Numeric values outside configured min/max
- **Pattern**: String values not matching required regex
- **Uniqueness**: Duplicate values in column marked unique
- **Severity**: Error for constraint violations

**Empty or Constant Columns:**
- **Empty**: All values are NULL or empty
- **Constant**: All non-NULL values are identical
- **Severity**: Info

**High Cardinality:**
- **Definition**: Number of unique values >90% of row count (potential identifier)
- **Severity**: Info

#### 1.2.2 Quality Score Calculation

**Formula:**
```
quality_score = 100 - (
    (missing_penalty * missing_percentage) +
    (duplicate_penalty * duplicate_percentage) +
    (error_penalty * error_count / row_count * 100)
)

Where:
- missing_penalty = 0.5 (0.5 points per 1% missing)
- duplicate_penalty = 0.3 (0.3 points per 1% duplicate)
- error_penalty = 10 (10 points per error per row, normalized)
- quality_score clamped to [0, 100]
```

**Interpretation:**
- **90-100**: Excellent
- **75-89**: Good
- **60-74**: Fair
- **<60**: Poor

---

### 1.3 PII Category Specifications

#### 1.3.1 Email Addresses

**Definition**: Electronic mail address in format `local-part@domain`

**Detection Pattern (Rule-Based):**
```regex
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
```

**Validation:**
- Local part: 1-64 characters, alphanumeric and special characters (`._%+-`)
- Domain: Valid domain structure (alphanumeric, hyphens, dots)
- TLD: At least 2 characters

**Examples:**
- ✅ Valid: `john.doe@example.com`, `user+tag@sub.domain.co.uk`
- ❌ Invalid: `@example.com`, `user@`, `user@.com`, `user@domain`

**NLP Recognition**: PERSON + context clues, or direct pattern recognition (if NLP uses patterns, it's not purely NLP-based)

#### 1.3.2 Phone Numbers

**Definition**: Telephone number in various formats

**Detection Patterns (Rule-Based):**
```regex
# North American: (555) 123-4567, 555-123-4567, 5551234567
\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}

# International: +1-555-123-4567, +44 20 1234 5678
\+\d{1,3}[\s.-]?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,9}
```

**Validation:**
- Total digits: 10 (North American) or 7-15 (International)
- Optional country code prefix (`+`)
- Optional formatting (parentheses, hyphens, spaces)

**Examples:**
- ✅ Valid: `(555) 123-4567`, `555-123-4567`, `+1-555-123-4567`
- ❌ Invalid: `123-4567` (too short), `(555)123` (incomplete)

**NLP Recognition**: Limited (phone numbers are primarily pattern-based)

#### 1.3.3 Social Security Numbers (US)

**Definition**: US Social Security Number in format `AAA-GG-SSSS`

**Detection Pattern (Rule-Based):**
```regex
\b\d{3}-\d{2}-\d{4}\b
```

**Validation:**
- Area number (AAA): 001-899, excluding 666
- Group number (GG): 01-99
- Serial number (SSSS): 0001-9999
- Format: XXX-XX-XXXX or XXXXXXXXX

**Examples:**
- ✅ Valid: `123-45-6789`, `078-05-1120`
- ❌ Invalid: `000-12-3456`, `666-12-3456`, `123-00-0000`

**NLP Recognition**: Not applicable (SSNs are pattern-based)

#### 1.3.4 Credit Card Numbers

**Definition**: Payment card number (13-19 digits)

**Detection Pattern (Rule-Based):**
```regex
\b\d{13,19}\b  # Or with spacing/hyphens
\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b
```

**Validation:**
- Length: 13-19 digits (Visa: 16, Mastercard: 16, Amex: 15)
- Luhn algorithm checksum validation
- Optional formatting (4-digit groups)

**Examples:**
- ✅ Valid: `4532015112830366` (Visa, passes Luhn)
- ❌ Invalid: `1234567890123456` (fails Luhn), `123` (too short)

**NLP Recognition**: Not applicable (credit cards are pattern-based)

#### 1.3.5 IP Addresses

**Definition**: Internet Protocol address (IPv4 or IPv6)

**Detection Patterns (Rule-Based):**
```regex
# IPv4: 192.168.1.1
\b(?:\d{1,3}\.){3}\d{1,3}\b

# IPv6: 2001:0db8:85a3::8a2e:0370:7334
([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}
```

**Validation:**
- IPv4: Each octet 0-255
- IPv6: Valid hexadecimal format

**Examples:**
- ✅ Valid: `192.168.1.1`, `8.8.8.8`, `2001:0db8:85a3::8a2e:0370:7334`
- ❌ Invalid: `256.1.1.1`, `192.168.1`, `192.168.1.1.1`

**NLP Recognition**: Not applicable (IP addresses are pattern-based)

#### 1.3.6 Named Entities (NLP-Only)

**PERSON Names:**
- Detection: spaCy NER with label `PERSON`
- Confidence: Model-dependent (typically >0.5 for inclusion)
- Validation: None (rely on model)

**ORGANIZATION Names:**
- Detection: spaCy NER with label `ORG`
- Use case: Identifying company names that may be sensitive

**LOCATION Names:**
- Detection: spaCy NER with label `GPE` (Geo-Political Entity)
- Use case: Identifying cities, states, countries

**Note**: For fair comparison, the rule-based method does NOT attempt to detect person names (too unreliable with simple patterns). This is a differentiator for the NLP method.

---

### 1.4 Anonymization Strategies

#### 1.4.1 Masking

**Definition**: Replace characters with mask character while preserving structure

**Implementation:**
- **Email**: `john.doe@example.com` → `***@***.***` (or `j***@e***.com` for partial)
- **Phone**: `(555) 123-4567` → `(***) ***-****`
- **Credit Card**: `4532 0151 1283 0366` → `**** **** **** 0366` (last 4 visible)

**Properties:**
- Partially reversible (if mask key retained)
- Preserves format recognition
- Low utility for analysis

**Configuration:**
- `mask_char`: Character to use (default: `*`)
- `partial`: Preserve some characters (e.g., last 4 of CC)

#### 1.4.2 Redaction

**Definition**: Complete removal or replacement with placeholder

**Implementation:**
- **Email**: `john.doe@example.com` → `[REDACTED]` or `[EMAIL]`
- **Phone**: `(555) 123-4567` → `[REDACTED]` or empty string
- **SSN**: `123-45-6789` → `[SSN]`

**Properties:**
- Irreversible
- No format preservation
- Zero utility for original value

**Configuration:**
- `placeholder`: Text to use (default: `[REDACTED]`)
- `category_label`: Use category name (e.g., `[EMAIL]`, `[PHONE]`)

#### 1.4.3 Pseudonymization

**Definition**: Consistent deterministic replacement using cryptographic hash

**Implementation:**
```python
import hashlib
import hmac

def pseudonymize(value: str, key: str, category: str) -> str:
    """Generate consistent pseudonym for value."""
    mac = hmac.new(key.encode(), f"{category}:{value}".encode(), hashlib.sha256)
    hash_hex = mac.hexdigest()[:16]  # Use first 16 chars
    return f"{category}_{hash_hex}"
```

**Example:**
- `john.doe@example.com` → `EMAIL_a3f5e9d2c1b4f6e8`
- Same email always maps to same pseudonym (if same key)
- Different emails map to different pseudonyms

**Properties:**
- Reversible only with key (not truly anonymous)
- Preserves uniqueness (one-to-one mapping)
- Preserves relationships (same email in multiple rows stays consistent)
- Higher utility for analysis (can still join, count unique)

**Configuration:**
- `key`: HMAC key (secret, stored securely)
- `algorithm`: Hash algorithm (default: SHA-256)

**Security Note**: Pseudonymization is reversible (not anonymization). Use only when consistent identifiers needed and key secured.

#### 1.4.4 Generalization

**Definition**: Replace specific value with broader category

**Implementation:**
- **Email**: `john.doe@example.com` → `[EMAIL]`
- **Phone**: `(555) 123-4567` → `[PHONE]`
- **Age**: `27` → `20-30` (for numeric generalization)
- **ZIP**: `94103` → `94***` (for geo generalization)

**Properties:**
- Irreversible
- Reduces precision
- Moderate utility (category still known)

**Configuration:**
- `category_label`: Label to use per PII type

---

### 1.5 Processed Data Outputs

#### 1.5.1 Processed Dataset

**Format**: Same as input (CSV or JSON)

**Content**: Original data with PII transformed according to configured strategies

**Metadata**: Appended columns (optional):
- `_pii_detected`: Boolean (was PII detected in this row?)
- `_pii_types`: List of PII types detected (e.g., `['email', 'phone']`)

**Example:**
```csv
customer_id,name,email,phone,_pii_detected,_pii_types
1001,John Doe,***@***,***-***-****,true,"email,phone"
1002,Jane Smith,***@***,***-***-****,true,"email,phone"
```

#### 1.5.2 Data Quality Report

**Format**: JSON

**Structure:**
```json
{
  "dataset_id": "abc123",
  "timestamp": "2026-10-25T14:32:15Z",
  "row_count": 10523,
  "column_count": 12,
  "quality_score": 85.3,
  "issues": [
    {
      "severity": "warning",
      "category": "missing",
      "column": "email",
      "description": "234 missing values (2.2%)",
      "count": 234
    }
  ],
  "column_stats": {
    "email": {
      "missing": 234,
      "unique": 10234,
      "type": "string"
    }
  }
}
```

#### 1.5.3 PII Detection Report

**Format**: JSON

**Structure:**
```json
{
  "run_id": "run_20261025_143215",
  "method": "rule-based",
  "timestamp": "2026-10-25T14:32:15Z",
  "total_detections": 1234,
  "by_category": {
    "email": 456,
    "phone": 321,
    "ssn": 45
  },
  "by_column": {
    "email": {"email": 456},
    "phone": {"phone": 321},
    "notes": {"email": 12, "phone": 5, "ssn": 1}
  },
  "sample_detections": [
    {
      "row": 123,
      "column": "email",
      "type": "email",
      "preview": "j***@e***.com"
    }
  ]
}
```

#### 1.5.4 Transformation Audit

**Format**: JSON or CSV

**Structure:**
```json
{
  "run_id": "run_20261025_143215",
  "timestamp": "2026-10-25T14:32:15Z",
  "transformations_applied": 1234,
  "rows_affected": 987,
  "columns_affected": ["email", "phone", "ssn"],
  "by_type": {
    "email": {"strategy": "mask", "count": 456},
    "phone": {"strategy": "redact", "count": 321},
    "ssn": {"strategy": "pseudonymize", "count": 45}
  }
}
```

---

## 2. Research Specifications

### 2.1 Research Question

**Primary Question:**
> "How do rule-based and NLP-assisted PII detection methods compare in precision, recall, F1-score, and processing efficiency on a controlled dataset containing structured records and unstructured text?"

**Hypotheses:**
- **H1**: NLP-assisted method will achieve higher recall (detect more PII) than rule-based method
- **H2**: Rule-based method will achieve higher precision (fewer false positives) than NLP-assisted method
- **H3**: Rule-based method will process data significantly faster than NLP-assisted method
- **H4**: Performance differences will vary by PII category (e.g., email detection similar, name detection different)

**Null Hypotheses:**
- **H0**: No significant difference between methods in precision, recall, or F1-score

---

### 2.2 Experimental Design

#### 2.2.1 Methodology

**Type**: Comparative quantitative evaluation

**Independent Variable**: Detection method (rule-based vs. NLP-assisted)

**Dependent Variables**:
- Precision (per category and overall)
- Recall (per category and overall)
- F1-score (per category and overall)
- Processing time (total and per-record)
- False positive count
- False negative count

**Control Variables**:
- Same input dataset for both methods
- Same evaluation metrics and matching criteria
- Same hardware and software environment
- Repeated runs with fixed random seed for reproducibility

#### 2.2.2 Dataset Design

**Synthetic Dataset Generation:**

Use Faker library to generate realistic PII:
```python
from faker import Faker
fake = Faker()

# Generate samples
email = fake.email()
phone = fake.phone_number()
ssn = fake.ssn()
name = fake.name()
```

**Dataset Composition:**
- **Total records**: 5,000 (configurable)
- **Positive examples** (contain PII): 60% (3,000 records)
- **Negative examples** (no PII): 40% (2,000 records)

**PII Category Distribution (in positive examples):**
- Email: 40% (1,200)
- Phone: 30% (900)
- SSN: 15% (450)
- Credit Card: 10% (300)
- Person Name (NLP only): 30% (900)
- Mix of multiple PII types: 20% (600)

**Edge Cases and Adversarial Examples** (included in positive set):
- Malformed PII: `email@domain` (missing TLD), `555-1234` (incomplete phone)
- Ambiguous text: `"Call me at office"` (false trigger for phone)
- Noisy context: PII embedded in longer text
- Similar non-PII: `"user@localhost"`, `"123-45-6789 is not an SSN"`
- Whitespace and formatting variations: Extra spaces, tabs, line breaks

**Negative Examples:**
- Numeric sequences: `"123456789"` (not SSN format)
- Non-email text: `"contact at example dot com"`
- Non-phone text: `"reference number 555-1234-ABC"`
- Random text: Lorem ipsum, product descriptions, log messages

**Dataset Format:**
```json
{
  "records": [
    {
      "id": 1,
      "text": "Contact John Doe at john.doe@example.com or (555) 123-4567",
      "entities": [
        {"start": 8, "end": 16, "label": "PERSON", "text": "John Doe"},
        {"start": 20, "end": 43, "label": "EMAIL", "text": "john.doe@example.com"},
        {"start": 47, "end": 62, "label": "PHONE", "text": "(555) 123-4567"}
      ]
    },
    {
      "id": 2,
      "text": "Please send the report to our office",
      "entities": []  # Negative example
    }
  ]
}
```

**Ground Truth Annotation:**
- All PII locations marked with start/end positions and labels
- Generated programmatically during dataset creation
- Stored in JSON format for reproducibility
- Versioned and archived for future experiments

#### 2.2.3 Evaluation Protocol

**Pre-Experiment:**
1. Generate or load fixed evaluation dataset (with seed=42 for reproducibility)
2. Verify dataset integrity (expected PII counts, no generation errors)
3. Warm up NLP model (load model, process 10 samples, discard results)

**Experiment Execution:**
1. **Method A (Rule-Based)**:
   - Process entire dataset
   - Record start time
   - Collect all predictions
   - Record end time
   - Calculate elapsed time

2. **Method B (NLP-Assisted)**:
   - Process entire dataset
   - Record start time
   - Collect all predictions
   - Record end time
   - Calculate elapsed time

3. **Repeat**: Run each method 3 times, average timing results (excluding first warm-up run)

**Post-Experiment:**
1. Match predictions to ground truth using matching criteria
2. Calculate metrics for each method
3. Perform error analysis (sample FPs and FNs)
4. Generate comparison visualizations
5. Save results to database and JSON files

---

### 2.3 Evaluation Metrics

#### 2.3.1 Classification Metrics

**Precision:**
```
Precision = TP / (TP + FP)
```
- **Definition**: Proportion of detected PII that are actually PII
- **Interpretation**: High precision = few false alarms

**Recall:**
```
Recall = TP / (TP + FN)
```
- **Definition**: Proportion of actual PII that were detected
- **Interpretation**: High recall = few missed PII

**F1-Score:**
```
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```
- **Definition**: Harmonic mean of precision and recall
- **Interpretation**: Balanced measure of detection quality

**Per-Category Metrics:**
- Calculate precision, recall, F1 for each PII category separately
- **Macro-average**: Simple average across categories (equal weight per category)
- **Micro-average**: Aggregate TP, FP, FN across all categories, then calculate metrics

**Confusion Matrix:**
```
              Predicted
           Positive  Negative
Actual
Positive     TP        FN
Negative     FP        TN
```

#### 2.3.2 Matching Criteria

**Entity-Level Exact Matching:**
- **Match**: Predicted entity must have exact same start, end, and label as ground truth
- **Partial matches**: Not counted as TP (count as FP + FN)

**Alternative: Relaxed Matching (Optional):**
- **Match**: Intersection over Union (IoU) ≥ 0.5 and same label
- **IoU**: `len(intersection) / len(union)` of character spans

**Handling Multiple Predictions:**
- Each ground truth entity can match at most one prediction
- If multiple predictions overlap same ground truth, choose highest confidence
- Unmatched predictions count as FP
- Unmatched ground truth count as FN

**Example:**
```
Ground Truth: "john.doe@example.com" [start=20, end=43, label="EMAIL"]
Prediction 1: "john.doe@example.com" [start=20, end=43, label="EMAIL"] → TP (exact match)
Prediction 2: "john.doe@example"     [start=20, end=36, label="EMAIL"] → FP (partial, if exact matching)
```

#### 2.3.3 Performance Metrics

**Processing Time:**
- **Total time**: Time to process entire dataset (seconds)
- **Per-record time**: Total time / number of records (seconds/record)
- **Throughput**: Records processed per second (records/sec)

**Measurement:**
```python
import time
start = time.perf_counter()
predictions = detector.detect(dataset)
end = time.perf_counter()
elapsed = end - start
```

**Repeated Runs:**
- Run each method 3-5 times
- Report mean, standard deviation, min, max
- Exclude first run (warm-up) for NLP method

**System Context:**
- Record Python version, library versions, CPU model, RAM
- Include in experiment report for reproducibility

---

### 2.4 Statistical Analysis

#### 2.4.1 Descriptive Statistics

**For each method:**
- Mean, median, standard deviation for timing
- Precision, recall, F1 (overall and per-category)
- Confusion matrix

**Comparison:**
- Difference in metrics (Method B - Method A)
- Relative difference percentage

**Example:**
```
| Metric    | Rule-Based | NLP-Assisted | Difference |
|-----------|------------|--------------|------------|
| Precision |    0.94    |     0.89     |   -0.05    |
| Recall    |    0.87    |     0.93     |   +0.06    |
| F1-Score  |    0.90    |     0.91     |   +0.01    |
| Time (s)  |    2.3     |    45.6      |  +43.3     |
```

#### 2.4.2 Error Analysis

**False Positives:**
- Sample and categorize FP errors
- Common patterns (e.g., "user@localhost" flagged as email)
- Frequency of each error type

**False Negatives:**
- Sample and categorize FN errors
- Common patterns (e.g., malformed phone numbers missed)
- Frequency of each error type

**Per-Category Analysis:**
- Which PII categories have highest/lowest precision and recall?
- Where do methods differ most?

**Qualitative Insights:**
- What types of errors does each method make?
- Are errors systematic or random?
- What are trade-offs between methods?

---

### 2.5 Threats to Validity

#### 2.5.1 Internal Validity

**Threat**: Dataset generation bias
- **Mitigation**: Use diverse Faker providers, include edge cases, manually review samples

**Threat**: Implementation bugs
- **Mitigation**: Unit tests for detectors, verify metrics calculation with known examples

**Threat**: Inconsistent evaluation environment
- **Mitigation**: Fixed random seed, same hardware, clean cache between runs

#### 2.5.2 External Validity

**Threat**: Synthetic data may not reflect real-world PII
- **Limitation**: Acknowledge that real data may have different error patterns, languages, formats
- **Mitigation**: Use realistic Faker data, include domain-specific patterns (e.g., company email domains)

**Threat**: Limited PII categories
- **Limitation**: Evaluation covers only 5-6 categories, not all possible PII types
- **Mitigation**: Document scope clearly, suggest future work for additional categories

**Threat**: English language only
- **Limitation**: Results do not generalize to other languages
- **Mitigation**: Document clearly, note that NLP models are language-specific

#### 2.5.3 Construct Validity

**Threat**: Metrics may not capture all aspects of "good" detection
- **Mitigation**: Use multiple metrics (precision, recall, F1), perform error analysis, consider utility trade-offs

**Threat**: Ground truth annotation errors
- **Mitigation**: Programmatic generation (no manual annotation errors), verify samples manually

---

### 2.6 Reproducibility Requirements

#### 2.6.1 Reproducibility Checklist

- [ ] Fixed random seed documented and used consistently
- [ ] All dependencies pinned with exact versions (`requirements.txt`)
- [ ] Dataset generation script included and documented
- [ ] Evaluation dataset archived (JSON file in `data/synthetic/`)
- [ ] Experiment configuration file included (`experiments/configs/experiment_config.yaml`)
- [ ] Evaluation script runnable via CLI (`python experiments/scripts/run_evaluation.py`)
- [ ] System information recorded (Python version, OS, hardware)
- [ ] Model versions documented (spaCy model, Presidio version)
- [ ] Metrics calculation validated with unit tests
- [ ] Results stored in database and exported to JSON
- [ ] Instructions to replicate experiments in README

#### 2.6.2 Reproducibility Instructions

**To reproduce experiments:**
```bash
# 1. Setup environment
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m spacy download en_core_web_lg

# 2. Generate dataset (or use provided)
python experiments/scripts/generate_dataset.py --seed 42 --size 5000 --output data/synthetic/eval_dataset.json

# 3. Run experiments
python experiments/scripts/run_evaluation.py --dataset data/synthetic/eval_dataset.json --methods rule-based,nlp-assisted --runs 3

# 4. View results
python experiments/scripts/generate_report.py --results experiments/results/run_20261025.json
```

**Expected Output:**
- Metrics JSON file: `experiments/results/metrics_<timestamp>.json`
- Figures: `reports/figures/precision_recall_comparison.png`, etc.
- Text report: `reports/experiment_report.md`

---

### 2.7 Research Report Outline

**Title**: Comparative Evaluation of Rule-Based and NLP-Assisted PII Detection Methods

**Sections:**

1. **Abstract** (200 words)
   - Problem, methods, results, conclusion

2. **Introduction**
   - Background on PII and privacy
   - Motivation for comparative study
   - Research question and objectives

3. **Related Work**
   - PII detection approaches in literature
   - Comparison of pattern-based vs. ML-based methods
   - Existing tools (Presidio, Microsoft SEAL, etc.)

4. **Methodology**
   - System architecture
   - Detection method descriptions (rule-based, NLP-assisted)
   - Dataset generation and annotation
   - Evaluation protocol and metrics
   - Experimental setup

5. **Results**
   - Overall metrics comparison (table and charts)
   - Per-category analysis
   - Confusion matrices
   - Timing comparison
   - Error analysis (sample FPs and FNs)

6. **Discussion**
   - Interpretation of results
   - Trade-offs between methods
   - Practical implications
   - Limitations of study

7. **Conclusion**
   - Summary of findings
   - Contributions
   - Future work

8. **References**
   - Cited papers, documentation, tools

**Length**: 10-15 pages (including figures and references)

---

### 2.8 Ethical Considerations

**Use of Synthetic Data:**
- **Rationale**: Avoid exposing real personal information
- **Limitation**: Synthetic data may not fully represent real-world PII complexity
- **Disclosure**: Clearly state that all data is synthetic in reports and UI

**Privacy by Design:**
- **No real PII**: Never use real personal data for testing or demonstration
- **Transparent processing**: Clearly explain what detection methods do
- **User control**: Users must explicitly trigger PII detection and anonymization

**Responsible Disclosure of Limitations:**
- **No guarantee of 100% detection**: Acknowledge that some PII may be missed
- **No anonymization guarantee**: Explain that transformations may not be irreversible or compliant with regulations
- **Tool purpose**: This is a research/portfolio project, not a production privacy compliance tool

**Academic Integrity:**
- **No fabricated results**: All results must be from actual experiments
- **Proper citations**: Credit sources for methods, libraries, inspiration
- **Reproducibility**: Provide sufficient detail for independent verification

---

### 2.9 Future Research Directions

**Suggested Extensions:**

1. **Additional PII Categories**: Passport numbers, driver's license numbers, biometric identifiers, medical record numbers

2. **Multi-Language Support**: Evaluate detection performance on non-English PII (e.g., French, German, Spanish)

3. **Real-World Datasets**: Evaluate on publicly available datasets with known PII (e.g., Enron emails with annotations)

4. **Hybrid Methods**: Combine rule-based and NLP-assisted approaches for better precision-recall trade-off

5. **Active Learning**: Use uncertain predictions to improve detectors iteratively

6. **Contextual Detection**: Use surrounding context to improve accuracy (e.g., "email:" label before address)

7. **Privacy-Utility Trade-offs**: Measure impact of anonymization on downstream ML model performance

8. **Differential Privacy**: Implement and evaluate differential privacy mechanisms

---

**Document Status**: Draft  
**Next Steps**: Review dataset generation and evaluation scripts before implementation  
**Dependencies**: Requires approved requirements and architecture specifications
