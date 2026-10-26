# UI/UX Specification
## Privacy-Aware Data Engineering Pipeline

**Version:** 1.0  
**Date:** October 25, 2026

---

## 1. Design Philosophy

### 1.1 Core Principles

**Professional & Trustworthy**
- Clean, uncluttered interfaces
- Consistent visual language
- Data-focused, not decorative
- Suitable for technical portfolio and research presentation

**Privacy-Conscious**
- Visual cues for sensitive operations
- Clear transformation previews
- Explicit user consent for data modifications
- Transparent processing steps

**Data-Engineering Focused**
- Emphasize pipeline stages and data flow
- Surface quality metrics prominently
- Make complex operations understandable
- Support exploratory analysis

**Research-Oriented**
- Present experimental results clearly
- Visualize comparisons effectively
- Enable reproducibility
- Document methodology visibly

### 1.2 Target User Experience

Users should feel confident that:
1. They understand what data is being processed
2. They can see what privacy operations were applied
3. They can trust the processing results
4. They can explain the system's behavior
5. They can reproduce experiments independently

---

## 2. Design System

### 2.1 Color Palette

**Primary Colors** (Privacy & Trust theme)
- **Primary Blue**: `#2E5CFF` - Primary actions, key metrics
- **Dark Blue**: `#1E3A8A` - Headers, important text
- **Light Blue**: `#EFF6FF` - Background highlights, info panels

**Semantic Colors**
- **Success Green**: `#10B981` - Successful operations, positive metrics
- **Warning Yellow**: `#F59E0B` - Warnings, cautions
- **Error Red**: `#EF4444` - Errors, critical issues
- **Info Gray**: `#6B7280` - Secondary information

**Neutral Colors**
- **Background**: `#FFFFFF` (white)
- **Secondary Background**: `#F9FAFB` (light gray)
- **Border**: `#E5E7EB` (medium gray)
- **Text Primary**: `#111827` (near black)
- **Text Secondary**: `#6B7280` (gray)

**PII Highlight Colors** (for detection visualization)
- **Email**: `#8B5CF6` (purple)
- **Phone**: `#3B82F6` (blue)
- **SSN**: `#EF4444` (red)
- **Credit Card**: `#F97316` (orange)
- **Generic PII**: `#EC4899` (pink)

### 2.2 Typography

**Font Family**
- Primary: System font stack
  ```css
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
               "Helvetica Neue", Arial, sans-serif;
  ```
- Monospace (for code, data): `"Courier New", Courier, monospace`

**Type Scale**
- **H1 (Page Title)**: 32px, bold, dark blue
- **H2 (Section Title)**: 24px, semi-bold, dark blue
- **H3 (Subsection)**: 20px, semi-bold, dark blue
- **Body**: 16px, regular, near black
- **Small**: 14px, regular, gray
- **Caption**: 12px, regular, gray

### 2.3 Spacing System

**Base unit**: 8px

- **xs**: 4px
- **sm**: 8px
- **md**: 16px
- **lg**: 24px
- **xl**: 32px
- **2xl**: 48px

**Layout Grid**
- Container max-width: 1200px (centered)
- Column gap: 16px
- Row gap: 24px

### 2.4 Component Styles

**Cards**
- Background: White
- Border: 1px solid #E5E7EB
- Border radius: 8px
- Padding: 16px
- Box shadow: subtle (0 1px 3px rgba(0,0,0,0.1))

**Buttons**
- Primary: Blue background, white text, rounded
- Secondary: White background, blue border, blue text
- Danger: Red background, white text, rounded
- Padding: 8px 16px
- Border radius: 6px

**Metric Cards**
- Large number (32px, bold)
- Label below (14px, gray)
- Optional icon or trend indicator
- Colored accent based on semantic meaning

**Tables**
- Header: Gray background, bold text
- Rows: Alternating white/light gray
- Border: Light gray
- Hover: Subtle blue tint

**Charts**
- Plotly with custom color scheme
- Clear axis labels and legends
- Interactive tooltips
- Responsive sizing

---

## 3. Page Structure

### 3.1 Global Layout

```
┌───────────────────────────────────────────────────┐
│  Sidebar (Navigation)     │   Main Content Area   │
│                           │                       │
│  ┌──────────────────┐    │  ┌─────────────────┐ │
│  │  Logo / Title    │    │  │  Page Header    │ │
│  └──────────────────┘    │  └─────────────────┘ │
│                           │                       │
│  Navigation Links:        │  ┌─────────────────┐ │
│  • Home                   │  │                 │ │
│  • Upload                 │  │   Page Content  │ │
│  • Data Quality           │  │                 │ │
│  • PII Detection          │  │                 │ │
│  • Anonymization          │  │                 │ │
│  • Method Comparison      │  │                 │ │
│  • Experiments            │  │                 │ │
│  • Settings               │  │                 │ │
│                           │  └─────────────────┘ │
│  ┌──────────────────┐    │                       │
│  │  System Status   │    │                       │
│  └──────────────────┘    │                       │
└───────────────────────────────────────────────────┘
```

**Sidebar** (Width: 250px)
- Fixed position
- Logo/title at top
- Navigation links with icons
- Active page highlighted
- System status indicator at bottom (optional)

**Main Content** (Flex width, max 1200px)
- Page header (title + breadcrumb/context)
- Content area (scrollable)
- Footer (optional)

### 3.2 Responsive Behavior

- **Desktop (>1024px)**: Sidebar visible, full-width content
- **Tablet (768-1024px)**: Collapsible sidebar, adjusted content width
- **Mobile (<768px)**: Streamlit default responsive behavior (sidebar as drawer)

---

## 4. Page Specifications

### 4.1 Home / Overview Page

**Purpose**: Introduction, feature overview, quick start guidance

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Privacy-Aware Data Engineering Pipeline    │
│  [Tagline: Build, Detect, Anonymize, Eval] │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  What This Application Does                 │
│  • Ingests structured datasets              │
│  • Analyzes data quality                    │
│  • Detects PII using rule-based and NLP     │
│  • Applies privacy transformations          │
│  • Evaluates detection methods              │
└─────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Upload      │  │  Quality     │  │  Detection   │
│  Your Data   │  │  Analysis    │  │  & Privacy   │
│  [Icon]      │  │  [Icon]      │  │  [Icon]      │
└──────────────┘  └──────────────┘  └──────────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Research    │  │  Export      │  │  Reproduce   │
│  Evaluation  │  │  Results     │  │  Experiments │
│  [Icon]      │  │  [Icon]      │  │  [Icon]      │
└──────────────┘  └──────────────┘  └──────────────┘

┌─────────────────────────────────────────────┐
│  Quick Start Guide                          │
│  1. Upload CSV or JSON file                 │
│  2. Review data quality report              │
│  3. Configure PII detection method          │
│  4. Apply anonymization                     │
│  5. Compare detection methods               │
└─────────────────────────────────────────────┘

[Get Started Button] → Navigate to Upload Page
```

**Components:**
- Hero section with project title and tagline
- Feature cards (3 columns, 2 rows)
- Quick start numbered list
- Call-to-action button
- Optional: Sample dataset links

**Empty State**: N/A (always shows content)

### 4.2 Upload Dataset Page

**Purpose**: File upload, preview, validation

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Upload Dataset                             │
│  [Breadcrumb: Home > Upload]                │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  📁 Upload File                             │
│  ┌─────────────────────────────────────┐   │
│  │  Drag and drop or click to browse  │   │
│  │  Supported: CSV, JSON               │   │
│  │  Max size: 50 MB                    │   │
│  └─────────────────────────────────────┘   │
│  [File Upload Widget]                       │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  File Information                           │
│  • Name: customers.csv                      │
│  • Size: 2.5 MB                             │
│  • Rows: 10,523                             │
│  • Columns: 12                              │
│  • Encoding: UTF-8                          │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Data Preview (First 100 rows)              │
│  [Paginated Table with columns]             │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Column Information                         │
│  Column Name    | Type     | Missing | Unique│
│  ────────────────────────────────────────── │
│  customer_id    | int      | 0       | 10523 │
│  name           | string   | 15      | 10234 │
│  email          | string   | 23      | 10456 │
│  ...                                         │
└─────────────────────────────────────────────┘

[Continue to Data Quality] [Cancel/Clear]
```

**Workflow:**
1. User uploads file
2. System validates file (type, size)
3. System loads and previews data
4. User reviews preview
5. User clicks "Continue to Data Quality"

**States:**
- **Empty**: Show upload widget, sample dataset links
- **Uploading**: Progress indicator
- **Uploaded**: Show preview and file info
- **Error**: Display error message, allow retry

**Validation Messages:**
- ✅ Success: "File uploaded successfully. 10,523 rows detected."
- ⚠️ Warning: "File contains 234 duplicate rows."
- ❌ Error: "File exceeds 50 MB limit. Please upload a smaller file."

### 4.3 Data Quality Page

**Purpose**: Profiling results, validation, cleaning

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Data Quality Analysis                      │
│  [Breadcrumb: Home > Upload > Quality]      │
└─────────────────────────────────────────────┘

┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐
│  Quality  │  │  Issues   │  │  Missing  │  │  Duplicates│
│  Score    │  │  Found    │  │  Values   │  │  Detected  │
│   85/100  │  │    12     │  │   234     │  │    56      │
│  [Good]   │  │  [⚠️]     │  │  [⚠️]     │  │  [⚠️]      │
└───────────┘  └───────────┘  └───────────┘  └───────────┘

┌─────────────────────────────────────────────┐
│  Issues by Severity                         │
│  [Stacked Bar Chart]                        │
│   Errors: 3   Warnings: 9   Info: 0        │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Issues Detail                              │
│  Severity | Category  | Description         │
│  ──────────────────────────────────────────│
│  ❌ Error | Missing   | Column 'email' has  │
│           |           | 234 missing values  │
│  ⚠️ Warning| Duplicate | 56 duplicate rows  │
│           |           | found (based on ID) │
│  ⚠️ Warning| Type      | Column 'age' has   │
│           |           | 3 non-numeric values│
│  ...                                        │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Missing Values by Column                   │
│  [Horizontal Bar Chart]                     │
│   email    ████████░░ 234 (2.2%)            │
│   phone    ██░░░░░░░░  45 (0.4%)            │
│   address  ████░░░░░░ 123 (1.2%)            │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Data Cleaning (Optional)                   │
│  ☐ Remove duplicate rows                    │
│  ☐ Fill missing values (Strategy: [Dropdown])│
│  ☐ Drop columns: [Multi-select]            │
│  [Apply Cleaning]                           │
└─────────────────────────────────────────────┘

[Continue to PII Detection] [Back] [Download Report]
```

**Components:**
- Metric cards (4 across)
- Issues by severity chart
- Issues detail table (sortable, filterable)
- Missing values chart
- Optional cleaning actions
- Navigation buttons

**Empty State**: If no issues found, show success message and checkmark

### 4.4 PII Detection Page

**Purpose**: Configure detection, view results, category distribution

**Layout:**
```
┌─────────────────────────────────────────────┐
│  PII Detection                              │
│  [Breadcrumb: Home > ... > Detection]       │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Detection Method                           │
│  ◉ Rule-Based (Fast, Pattern Matching)      │
│  ○ NLP-Assisted (Slower, More Accurate)     │
│                                             │
│  PII Categories to Detect:                  │
│  ☑ Email Addresses                          │
│  ☑ Phone Numbers                            │
│  ☑ Social Security Numbers                  │
│  ☑ Credit Card Numbers                      │
│  ☑ IP Addresses                             │
│                                             │
│  [Run Detection]                            │
└─────────────────────────────────────────────┘

┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐
│  Total    │  │  Emails   │  │  Phones   │  │  SSNs     │
│  PII Found│  │  Detected │  │  Detected │  │  Detected │
│   1,234   │  │    456    │  │    321    │  │    45     │
└───────────┘  └───────────┘  └───────────┘  └───────────┘

┌─────────────────────────────────────────────┐
│  PII Distribution by Category               │
│  [Pie Chart or Stacked Bar]                 │
│   Email: 456 (37%)                          │
│   Phone: 321 (26%)                          │
│   SSN: 45 (3.6%)                            │
│   ...                                       │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  PII Detection by Column                    │
│  Column     | Email | Phone | SSN | CC | IP │
│  ──────────────────────────────────────────│
│  email      |  456  |   0   |  0  |  0 |  0 │
│  phone      |   0   |  321  |  0  |  0 |  0 │
│  notes      |  12   |   5   |  1  |  0 |  2 │
│  ...                                        │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Sample Detections (Redacted)               │
│  Row  | Column | Type  | Preview             │
│  ──────────────────────────────────────────│
│  123  | email  | EMAIL | j***@***.com        │
│  456  | phone  | PHONE | (***) ***-1234      │
│  ...                                        │
└─────────────────────────────────────────────┘

[Continue to Anonymization] [Back] [Download Results]
```

**Workflow:**
1. User selects detection method
2. User selects PII categories
3. User clicks "Run Detection"
4. System processes (show progress)
5. System displays results

**States:**
- **Configuration**: Show method and category selection
- **Processing**: Progress indicator, estimated time
- **Results**: Show metrics, charts, tables

**Empty State**: If no PII detected, show message "No PII detected in this dataset."

### 4.5 Anonymization Page

**Purpose**: Configure transformations, preview, apply, audit

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Anonymization Configuration                │
│  [Breadcrumb: Home > ... > Anonymization]   │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Transformation Strategy by PII Type        │
│  PII Type       | Strategy       | Preview  │
│  ──────────────────────────────────────────│
│  Email          | [Mask ▼]       | ***@***  │
│  Phone          | [Redact ▼]     | [PHONE]  │
│  SSN            | [Pseudonymize] | Hash123  │
│  Credit Card    | [Mask ▼]       | ****1234 │
│  IP Address     | [Generalize ▼] | [IP]     │
│                                             │
│  [Apply Transformations]                    │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Preview: Before and After                  │
│  [Side-by-side table showing sample rows]   │
│  Before:                    After:          │
│  john.doe@example.com  →  ***@***.***       │
│  (555) 123-4567        →  [REDACTED]        │
│  123-45-6789           →  a3f5e...          │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Transformation Summary                     │
│  • Total transformations: 1,234             │
│  • Rows affected: 987                       │
│  • Columns affected: email, phone, ssn      │
│  • Method: Rule-based                       │
│  • Timestamp: 2026-10-25 14:32:15           │
└─────────────────────────────────────────────┘

┌───────────┐  ┌───────────┐  ┌───────────┐
│  Masked   │  │  Redacted │  │ Pseudonym │
│    456    │  │    321    │  │    45     │
└───────────┘  └───────────┘  └───────────┘

┌─────────────────────────────────────────────┐
│  Transformation Audit Log                   │
│  Type  | Strategy | Count | Column          │
│  ──────────────────────────────────────────│
│  EMAIL | Mask     |  456  | email           │
│  PHONE | Redact   |  321  | phone           │
│  SSN   | Pseudo   |   45  | ssn             │
│  ...                                        │
└─────────────────────────────────────────────┘

[Continue to Export] [Back] [Download Audit]
```

**Workflow:**
1. User configures strategies per PII type
2. User previews transformations
3. User applies transformations
4. System shows audit summary

**Interactive Elements:**
- Strategy dropdowns per PII type
- Preview before applying
- Confirmation dialog for Apply

**Empty State**: If no PII detected, show message "No PII to anonymize."

### 4.6 Method Comparison Page

**Purpose**: Visual comparison of rule-based vs NLP-assisted detection

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Detection Method Comparison                │
│  [Breadcrumb: Home > ... > Comparison]      │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Methods Compared                           │
│  • Rule-Based: Pattern matching + validation│
│  • NLP-Assisted: Presidio + spaCy NER       │
│  • Dataset: Current uploaded dataset        │
│  • Categories: Email, Phone, SSN, CC, IP    │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Detection Count Comparison                 │
│  [Grouped Bar Chart]                        │
│   Category    | Rule-Based | NLP-Assisted   │
│   Email       |    456     |     478        │
│   Phone       |    321     |     305        │
│   SSN         |     45     |      52        │
│   ...                                       │
└─────────────────────────────────────────────┘

┌────────────────────┐  ┌────────────────────┐
│  Rule-Based        │  │  NLP-Assisted      │
│  • Total: 1,234    │  │  • Total: 1,298    │
│  • Time: 2.3s      │  │  • Time: 45.6s     │
│  • Speed: Fast     │  │  • Speed: Moderate │
└────────────────────┘  └────────────────────┘

┌─────────────────────────────────────────────┐
│  Qualitative Comparison                     │
│  Feature        | Rule-Based | NLP-Assisted │
│  ──────────────────────────────────────────│
│  Speed          |   Fast     |   Moderate   │
│  Accuracy       |   High*    |   Higher*    │
│  False Positives|   Low      |   Medium     │
│  Flexibility    |   Limited  |   High       │
│  Setup          |   Simple   |   Complex    │
│  *Requires ground truth evaluation          │
└─────────────────────────────────────────────┘

[Run Both Methods] [View Experiment Results] [Back]
```

**Components:**
- Method descriptions
- Detection count comparison (grouped bar chart)
- Summary cards (side-by-side)
- Qualitative comparison table
- Link to detailed experiments page

**Note**: This page shows exploratory comparison on uploaded data. For rigorous evaluation, direct users to Experiments page.

### 4.7 Experiment Results Page

**Purpose**: Detailed experimental evaluation with ground truth

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Experimental Evaluation Results            │
│  [Breadcrumb: Home > ... > Experiments]     │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Experiment Configuration                   │
│  • Dataset: Synthetic evaluation set (5,000)│
│  • Methods: Rule-Based vs. NLP-Assisted     │
│  • Metrics: Precision, Recall, F1, Timing   │
│  • Date: 2026-10-25                         │
│  [Re-run Experiments] [Load Saved Results]  │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Overall Performance Metrics                │
│  [Side-by-side comparison]                  │
│  Metric       | Rule-Based | NLP-Assisted   │
│  ──────────────────────────────────────────│
│  Precision    |   0.94     |     0.89       │
│  Recall       |   0.87     |     0.93       │
│  F1-Score     |   0.90     |     0.91       │
│  Processing   |   2.3s     |    45.6s       │
│  Time         |            |                │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Precision, Recall, F1 Comparison           │
│  [Grouped Bar Chart]                        │
│   Metric    | Rule-Based | NLP-Assisted     │
│   Precision |   0.94     |     0.89         │
│   Recall    |   0.87     |     0.93         │
│   F1        |   0.90     |     0.91         │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Per-Category Performance                   │
│  [Heatmap or table]                         │
│  Category  | Method        | Prec | Rec | F1│
│  ──────────────────────────────────────────│
│  Email     | Rule-Based    | 0.98 |0.95|0.96│
│  Email     | NLP-Assisted  | 0.92 |0.97|0.94│
│  Phone     | Rule-Based    | 0.96 |0.89|0.92│
│  Phone     | NLP-Assisted  | 0.88 |0.91|0.89│
│  ...                                        │
└─────────────────────────────────────────────┘

┌────────────────────┐  ┌────────────────────┐
│  Rule-Based        │  │  NLP-Assisted      │
│  Confusion Matrix  │  │  Confusion Matrix  │
│  [Heatmap]         │  │  [Heatmap]         │
│         Predicted  │  │         Predicted  │
│  Actual   P    N   │  │  Actual   P    N   │
│    P    850   50   │  │    P    920   80   │
│    N     30  3070  │  │    N    120  2880  │
└────────────────────┘  └────────────────────┘

┌─────────────────────────────────────────────┐
│  Error Analysis                             │
│  False Positives (Sample):                  │
│  • "Call me at office" (detected as phone)  │
│  • "user@localhost" (detected as email)     │
│                                             │
│  False Negatives (Sample):                  │
│  • "555.123.4567" (not detected)            │
│  • Misspelled email formats                 │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Processing Time Comparison                 │
│  [Bar Chart]                                │
│  Rule-Based:    ████░░░░░░ 2.3s             │
│  NLP-Assisted:  █████████████████ 45.6s     │
└─────────────────────────────────────────────┘

[Download Results JSON] [Download Report PDF] [Back]
```

**Components:**
- Experiment configuration summary
- Overall metrics table (side-by-side)
- Performance comparison charts
- Per-category metrics table/heatmap
- Confusion matrices (side-by-side)
- Error analysis (sample FPs and FNs)
- Processing time comparison
- Download options

**Empty State**: "No experiment results available. Please run experiments first."

**Note**: This page shows actual scientific evaluation results with ground truth, not just exploratory comparison.

### 4.8 Settings / History Page (Optional)

**Purpose**: Configuration, processing history, system status

**Layout:**
```
┌─────────────────────────────────────────────┐
│  Settings & History                         │
│  [Breadcrumb: Home > Settings]              │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Application Settings                       │
│  Max File Size: [50] MB                     │
│  Max Rows: [100000]                         │
│  Default Detection Method: [Rule-Based ▼]   │
│  [Save Settings]                            │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Processing History (Last 10 runs)          │
│  Date       | Dataset    | Method | Status  │
│  ──────────────────────────────────────────│
│  2026-10-25 | customers  | Rule   | Success │
│  2026-10-24 | orders     | NLP    | Success │
│  2026-10-23 | users      | Rule   | Failed  │
│  ...                                        │
│  [View Details] [Delete Old Runs]           │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  System Status                              │
│  • Python Version: 3.11.5                   │
│  • Streamlit Version: 1.28.0                │
│  • spaCy Model: en_core_web_lg (installed)  │
│  • DuckDB: Connected                        │
│  • Database Size: 12.5 MB                   │
└─────────────────────────────────────────────┘

[Clear Cache] [Export Database] [Back to Home]
```

**Optional Features:**
- User preferences
- Processing history with details
- System diagnostics
- Database management
- Cache clearing

---

## 5. Component Library

### 5.1 Metric Card Component

**Purpose**: Display KPI or metric with label

**Props:**
- `value`: Number or string to display
- `label`: Descriptive text
- `icon`: Optional icon
- `color`: Semantic color (success, warning, error, info)
- `trend`: Optional trend indicator (↑, ↓, →)

**Example:**
```python
metric_card(
    value="1,234",
    label="PII Instances Detected",
    icon="🔍",
    color="info"
)
```

### 5.2 Data Table Component

**Purpose**: Display paginated, sortable data

**Props:**
- `data`: DataFrame to display
- `columns`: List of columns to show (optional, default: all)
- `page_size`: Rows per page (default: 25)
- `sortable`: Enable sorting (default: True)
- `highlight_columns`: List of columns to highlight
- `redact`: Redact sensitive columns (optional)

**Example:**
```python
data_table(
    data=df,
    columns=['id', 'name', 'email'],
    page_size=25,
    highlight_columns=['email'],
    redact=['email']
)
```

### 5.3 Chart Component

**Purpose**: Wrapper for Plotly charts with consistent styling

**Types:**
- `bar_chart(data, x, y, title)`
- `line_chart(data, x, y, title)`
- `pie_chart(data, names, values, title)`
- `heatmap(data, x, y, z, title)`
- `confusion_matrix(y_true, y_pred, labels)`

**Example:**
```python
bar_chart(
    data=df,
    x='category',
    y='count',
    title='PII Distribution by Category',
    color='category'
)
```

### 5.4 Feedback Component

**Purpose**: Display success, warning, error messages

**Types:**
- `success(message, details=None)`
- `warning(message, details=None)`
- `error(message, details=None, traceback=False)`
- `info(message, details=None)`

**Example:**
```python
success(
    message="Dataset uploaded successfully",
    details="10,523 rows, 12 columns detected"
)
```

### 5.5 Progress Indicator Component

**Purpose**: Show processing progress

**Types:**
- `progress_bar(value, max_value, label)`
- `spinner(message)`
- `stage_indicator(stages, current_stage)`

**Example:**
```python
stage_indicator(
    stages=['Ingest', 'Profile', 'Detect', 'Transform', 'Report'],
    current_stage=2  # Detecting
)
```

---

## 6. User Journeys

### 6.1 Primary Journey: Upload and Process Dataset

1. **Home Page**: User reads overview, clicks "Get Started"
2. **Upload Page**: User uploads CSV file, reviews preview
3. **Data Quality Page**: User views quality report, optionally cleans data
4. **PII Detection Page**: User selects rule-based method, runs detection
5. **Anonymization Page**: User configures masking strategies, applies transformations
6. **Download**: User exports processed dataset

**Expected Time**: 5-10 minutes for typical dataset

### 6.2 Secondary Journey: Compare Detection Methods

1. **Home Page**: User navigates to "Method Comparison"
2. **Comparison Page**: User sees high-level comparison, clicks "View Experiment Results"
3. **Experiments Page**: User reviews detailed metrics, confusion matrices
4. **Download**: User exports experiment results

**Expected Time**: 2-5 minutes

### 6.3 Research Journey: Run Custom Experiment

1. **Experiments Page**: User clicks "Re-run Experiments"
2. **Configuration**: User adjusts experiment parameters
3. **Execution**: System generates dataset, runs both methods, calculates metrics
4. **Results**: User views updated metrics and charts
5. **Download**: User exports results for research report

**Expected Time**: 5-15 minutes (depending on dataset size)

---

## 7. Interaction Patterns

### 7.1 Form Interactions

- **Submit buttons**: Primary blue, right-aligned
- **Cancel buttons**: Secondary gray, left of submit
- **Validation**: Inline errors below fields
- **Required fields**: Asterisk or "(required)" label
- **Help text**: Small gray text below fields

### 7.2 Table Interactions

- **Sorting**: Click column header to toggle sort
- **Filtering**: Search box above table
- **Pagination**: Controls below table (← 1 2 3 ... →)
- **Selection**: Checkboxes for multi-select (if needed)
- **Row actions**: Icons in last column (view, delete)

### 7.3 Chart Interactions

- **Tooltips**: Hover to see detailed values
- **Zoom**: Click and drag to zoom (Plotly default)
- **Pan**: Hold shift and drag to pan
- **Reset**: Double-click to reset zoom
- **Download**: Plotly camera icon to save as PNG

### 7.4 Navigation

- **Sidebar links**: Highlight active page
- **Breadcrumbs**: Show current location, clickable to go back
- **Back buttons**: Navigate to previous step in workflow
- **Stepper/progress**: Visual indicator of multi-step process

---

## 8. Responsive Design

### 8.1 Breakpoints

- **Desktop**: >1024px — Full sidebar, multi-column layouts
- **Tablet**: 768-1024px — Collapsible sidebar, 2-column layouts
- **Mobile**: <768px — Drawer sidebar, single-column layouts

### 8.2 Mobile Considerations

- **Tables**: Horizontal scroll or card layout
- **Charts**: Reduce size, simplify legends
- **Forms**: Stack fields vertically
- **Buttons**: Full-width on mobile
- **Metric cards**: 1-2 per row instead of 4

**Note**: Primary target is desktop/laptop. Mobile support is secondary (Streamlit default behavior acceptable).

---

## 9. Accessibility

### 9.1 Color Contrast

- Ensure WCAG AA compliance (4.5:1 for normal text, 3:1 for large text)
- Do not rely solely on color to convey information
- Use icons and labels in addition to colors

### 9.2 Semantic HTML

- Use proper heading hierarchy (H1 > H2 > H3)
- Use descriptive link text ("Download report" not "Click here")
- Use ARIA labels where appropriate (Streamlit handles most)

### 9.3 Keyboard Navigation

- All interactive elements focusable via Tab
- Logical tab order
- Visible focus indicators
- Streamlit provides keyboard support by default

### 9.4 Screen Reader Support

- Alt text for images (if any)
- ARIA labels for icons
- Descriptive button labels
- Table headers properly marked up

**Note**: Full accessibility audit requires user testing with assistive technologies. Aim for reasonable accessibility using Streamlit's built-in support.

---

## 10. Error States and Empty States

### 10.1 Error States

**Upload Error:**
- Icon: ❌
- Message: "Failed to upload file: File exceeds 50 MB limit."
- Action: "Please upload a smaller file or adjust settings."

**Processing Error:**
- Icon: ⚠️
- Message: "PII detection failed: NLP model not found."
- Action: "Install model with: `python -m spacy download en_core_web_lg`"

**Validation Error:**
- Icon: ⚠️
- Message: "Data validation failed: Column 'email' has invalid formats."
- Action: "Review data quality report and clean data."

### 10.2 Empty States

**No Data Uploaded:**
- Icon: 📁
- Message: "No dataset uploaded yet."
- Action: "Upload a CSV or JSON file to get started." [Upload Button]

**No PII Detected:**
- Icon: ✅
- Message: "No PII detected in this dataset."
- Action: "Your data appears to be clean. Proceed to export."

**No Experiment Results:**
- Icon: 🔬
- Message: "No experiment results available."
- Action: "Run experiments to compare detection methods." [Run Experiments Button]

---

## 11. Loading States

### 11.1 Upload Loading

- Progress bar showing upload percentage
- Message: "Uploading file... 45%"

### 11.2 Processing Loading

- Spinner with stage indicator
- Message: "Processing dataset... Detecting PII (Step 3/5)"
- Estimated time: "Estimated time: ~30 seconds"

### 11.3 Experiment Loading

- Progress bar with sub-steps
- Message: "Running experiments..."
  - "Generating synthetic dataset... ✓"
  - "Running rule-based detection... ⏳"
  - "Running NLP detection..."
  - "Calculating metrics..."

---

## 12. Design System Implementation

### 12.1 Streamlit Custom CSS

**Location**: `.streamlit/config.toml` and custom CSS file

**Strategy:**
- Use Streamlit's theming system for global colors
- Add custom CSS for fine-grained control
- Keep custom CSS minimal and maintainable

**Example `config.toml`:**
```toml
[theme]
primaryColor="#2E5CFF"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F9FAFB"
textColor="#111827"
font="sans serif"
```

**Custom CSS (if needed):**
```css
/* Metric cards */
.metric-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

/* PII highlight colors */
.pii-email { background-color: #EDE9FE; }
.pii-phone { background-color: #DBEAFE; }
.pii-ssn { background-color: #FEE2E2; }
```

### 12.2 Component Reusability

**Approach:**
1. Create reusable functions in `src/ui/components/`
2. Import and use across pages
3. Document component API and examples
4. Test components independently where possible

---

## 13. Visual Design References

### 13.1 Inspiration Sources (for research, not copying)

- **Data platforms**: Databricks, Snowflake, dbt Cloud (clean, data-focused)
- **Privacy tools**: OneTrust, TrustArc (trust and privacy themes)
- **Analytics dashboards**: Looker, Tableau, Mode (effective data visualization)
- **Design systems**: Material Design, Atlassian Design System (consistency)

**Note**: Use these as inspiration for design patterns, not for copying specific designs.

### 13.2 Design Deliverables for Implementation

Before implementation, create:
1. **Color palette swatch** (hex codes for all colors)
2. **Typography scale** (sizes and weights for all text elements)
3. **Component inventory** (list and specs of reusable components)
4. **Page wireframes** (low-fidelity sketches for each page)
5. **Example screenshots** (from similar tools for reference)

---

## 14. Usability Testing Plan

### 14.1 Test Scenarios

1. **First-time user**: Can they understand purpose and complete primary workflow?
2. **Technical reviewer**: Can they understand detection methodology and results?
3. **Research evaluator**: Can they interpret experiment results and reproduce?

### 14.2 Usability Metrics

- **Task completion rate**: % of users who complete primary workflow
- **Time on task**: Minutes to upload, process, and export dataset
- **Error rate**: Number of user errors or confusions
- **Satisfaction**: Subjective rating (1-5 scale)

### 14.3 Testing Method

- **Moderated usability testing**: Observe users, ask for feedback
- **Think-aloud protocol**: Users narrate their thought process
- **Post-test questionnaire**: Collect satisfaction and feedback

**Note**: For portfolio project, informal testing with peers or mentors is sufficient.

---

## 15. Design Iteration Plan

### 15.1 MVP Design (Milestone 9)

- Core pages: Home, Upload, Quality, Detection, Anonymization
- Basic styling with Streamlit defaults
- Functional, not polished

### 15.2 Polished Design (Milestone 10-11)

- All pages complete
- Custom CSS for consistent branding
- Refined charts and visualizations
- Professional empty and error states

### 15.3 Final Refinement (Milestone 12)

- User testing feedback incorporated
- Screenshots for documentation
- Deployment-ready design
- Accessibility review

---

**Document Status**: Draft  
**Next Steps**: Review and create mockups/wireframes before implementation  
**Dependencies**: Requires approved architecture specification
