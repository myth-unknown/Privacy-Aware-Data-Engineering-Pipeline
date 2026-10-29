# Sample Datasets

This directory contains sample datasets for testing and demonstrating the Privacy-Aware Data Engineering Pipeline.

## Files

### 1. customers.csv
**Format:** CSV  
**Description:** Customer database with various types of PII  
**Rows:** 10  
**Columns:** 10

**PII Types Present:**
- Email addresses
- Phone numbers (US format)
- Physical addresses
- Social Security Numbers (SSN)
- Credit card numbers
- ZIP codes

**Use Case:** Ideal for testing PII detection and anonymization features.

---

### 2. orders.json
**Format:** JSON (array of records)  
**Description:** E-commerce order data with customer and payment information  
**Records:** 5  
**Fields:** 10 per record

**PII Types Present:**
- Email addresses
- Phone numbers (various formats)
- Shipping addresses
- Credit card numbers (various card types)
- IP addresses

**Use Case:** Test JSON loading and diverse PII pattern detection.

---

### 3. malformed.csv
**Format:** CSV (with intentional quality issues)  
**Description:** Dataset with data quality problems for testing validation  
**Rows:** 8  
**Columns:** 7

**Quality Issues:**
- Duplicate column names
- Missing values in multiple columns
- Duplicate rows
- Fully empty row
- Inconsistent data types

**Use Case:** Test data quality validation and profiling features.

---

## Usage

You can use these files in the Streamlit UI:

1. Navigate to the **Upload Data** page
2. Upload one of these sample files
3. Observe the validation results and data preview
4. Continue through the pipeline to test PII detection and anonymization

## Data Generation

These datasets contain **synthetic data only**. No real personal information is included.
All PII values (SSNs, credit cards, addresses, emails) are fictional and generated for testing purposes.
