# Risk Register
## Privacy-Aware Data Engineering Pipeline

**Version:** 1.0  
**Date:** October 25, 2026

---

## Risk Assessment Matrix

**Probability Scale:**
- **Low (L)**: <20% chance of occurring
- **Medium (M)**: 20-50% chance
- **High (H)**: >50% chance

**Impact Scale:**
- **Low (L)**: Minor inconvenience, easily fixed
- **Medium (M)**: Significant effort to fix, delays milestone
- **High (H)**: Major blocker, requires architecture change

**Priority**: Probability × Impact

---

## Technical Risks

### R-1: NLP Model Compatibility Issues on Windows

**Category**: Technical - Dependencies  
**Probability**: High  
**Impact**: High  
**Priority**: **CRITICAL**

**Description**:
spaCy NLP models may have installation or runtime issues on Windows (PATH problems, C++ build tools, compatibility with Python 3.11).

**Consequences**:
- Milestone 5 blocked
- NLP-assisted detection unavailable
- Cannot complete research comparison
- May require different model or Python version

**Mitigation**:
- Test spaCy installation early (during Milestone 1)
- Document installation steps for Windows
- Prepare fallback: use smaller model (`en_core_web_md` instead of `en_core_web_lg`)
- Alternative: Use `en_core_web_sm` for testing if large model fails
- Last resort: Skip NLP method or use pattern-based Presidio recognizers only (less ideal for research)

**Contingency**:
- If spaCy fails completely, use only rule-based detection and document limitation
- Consider using Hugging Face Transformers with smaller NER model as alternative

**Owner**: Developer  
**Status**: Open

---

### R-2: Presidio Version Compatibility with Python 3.11

**Category**: Technical - Dependencies  
**Probability**: Medium  
**Impact**: High  
**Priority**: **HIGH**

**Description**:
Microsoft Presidio may not be fully compatible with Python 3.11 (library still catching up with latest Python versions).

**Consequences**:
- Milestone 5 blocked
- May need to downgrade to Python 3.10
- Dependency conflicts with other libraries

**Mitigation**:
- Check Presidio compatibility early (Milestone 1)
- Test installation: `pip install presidio-analyzer presidio-anonymizer`
- Review Presidio GitHub issues for Python 3.11 compatibility
- Be prepared to use Python 3.10 if needed

**Contingency**:
- Use Python 3.10 instead of 3.11 (minimal impact)
- Fork and patch Presidio if minor compatibility issues
- Use alternative NLP library (Hugging Face Transformers) if Presidio unusable

**Owner**: Developer  
**Status**: Open

---

### R-3: DuckDB File Locking in Multi-Session Scenarios

**Category**: Technical - Database  
**Probability**: Medium  
**Impact**: Medium  
**Priority**: **MEDIUM**

**Description**:
DuckDB may have file locking issues if multiple Streamlit sessions try to access the same database file simultaneously.

**Consequences**:
- Concurrent user sessions may fail
- Database corruption risk (low, but possible)
- Poor user experience if testing with multiple browser tabs

**Mitigation**:
- Use DuckDB's WAL (Write-Ahead Logging) mode
- Implement proper connection management (open/close per transaction)
- Test with multiple concurrent sessions during Milestone 7
- Document that application designed for single-user local use

**Contingency**:
- Use in-memory DuckDB for session-scoped operations
- Move to SQLite if DuckDB locking problematic
- For deployment: use separate database per session (session ID in filename)

**Owner**: Developer  
**Status**: Open

---

### R-4: Memory Consumption Exceeds 2GB on Large Datasets

**Category**: Technical - Performance  
**Probability**: Medium  
**Impact**: Medium  
**Priority**: **MEDIUM**

**Description**:
Processing 100K row datasets with multiple PII detections and NLP models may exceed 2GB RAM limit.

**Consequences**:
- Application crashes on large datasets
- Poor performance on machines with limited RAM
- Cannot demonstrate with realistic dataset sizes

**Mitigation**:
- Profile memory usage during Milestone 10
- Implement batch processing for large datasets (process in chunks)
- Use pandas chunking for file reading
- Release memory after each pipeline stage (explicit `del` and `gc.collect()`)
- Set realistic dataset size limits (e.g., 50K rows instead of 100K)

**Contingency**:
- Lower maximum dataset size to 50K rows
- Implement streaming/chunked processing
- Add memory usage warnings in UI
- Document memory requirements in README

**Owner**: Developer  
**Status**: Open

---

### R-5: Performance Degradation on Large Datasets

**Category**: Technical - Performance  
**Probability**: Medium  
**Impact**: Medium  
**Priority**: **MEDIUM**

**Description**:
Pipeline may take >5 minutes for 100K row datasets, especially with NLP detection.

**Consequences**:
- Poor user experience (long waits)
- May not meet performance targets
- Difficult to demonstrate with realistic data

**Mitigation**:
- Profile code during Milestone 10
- Optimize hot paths (regex compilation, vectorized operations)
- Use pandas vectorized operations instead of loops
- Cache NLP model and reuse
- Implement progress bars for long operations
- Set realistic expectations in documentation

**Contingency**:
- Lower maximum dataset size
- Implement background processing (if Streamlit supports)
- Add performance tips in UI (e.g., use rule-based for large datasets)
- Document performance characteristics clearly

**Owner**: Developer  
**Status**: Open

---

### R-6: False Positive Rate Too High

**Category**: Technical - Detection Quality  
**Probability**: Medium  
**Impact**: Medium  
**Priority**: **MEDIUM**

**Description**:
Rule-based or NLP detectors may produce too many false positives, reducing precision below acceptable levels.

**Consequences**:
- Poor detection quality metrics
- Research findings show both methods perform poorly
- Over-anonymization (removes non-PII data)

**Mitigation**:
- Implement contextual validation in rule-based detectors
- Tune NLP confidence thresholds during Milestone 5
- Include diverse test cases during evaluation
- Accept some false positives as realistic (document trade-offs)
- Provide user controls to adjust sensitivity

**Contingency**:
- Focus research on trade-offs between precision and recall
- Document that perfect detection is infeasible
- Allow users to review and adjust detection results before anonymization
- Emphasize learning and comparison over perfect accuracy

**Owner**: Developer  
**Status**: Open

---

### R-7: False Negative Rate Too High

**Category**: Technical - Detection Quality  
**Probability**: Medium  
**Impact**: Medium  
**Priority**: **MEDIUM**

**Description**:
Detectors may miss significant PII, resulting in low recall.

**Consequences**:
- Privacy risk (PII not detected or anonymized)
- Poor research metrics
- Application less useful for real-world scenarios

**Mitigation**:
- Test with diverse PII formats during development
- Include edge cases in evaluation dataset
- Tune detection patterns and thresholds
- Document limitations clearly
- Emphasize that tool is for research, not production privacy compliance

**Contingency**:
- Focus on specific PII categories where high recall achievable
- Document categories with known limitations
- Provide warnings in UI about missed PII
- Recommend manual review for sensitive data

**Owner**: Developer  
**Status**: Open

---

## Deployment Risks

### R-8: Streamlit Community Cloud Limitations

**Category**: Deployment  
**Probability**: High (if deploying)  
**Impact**: Medium  
**Priority**: **MEDIUM**

**Description**:
Streamlit Community Cloud has ephemeral filesystem, 1GB RAM limit, and limited CPU. DuckDB file won't persist, NLP model may be too large.

**Consequences**:
- Cannot use persistent DuckDB storage
- NLP model may not fit in memory
- Slow performance on cloud resources
- Deployment fails or is unusable

**Mitigation**:
- Treat deployment as optional (Milestone 12)
- Use in-memory DuckDB for deployment
- Use smaller spaCy model (`en_core_web_md` or `en_core_web_sm`)
- Limit dataset size for deployed version
- Provide clear disclaimer that deployed version is demo-only

**Contingency**:
- Deploy rule-based version only (no NLP)
- Use alternative hosting (Hugging Face Spaces, Render, Fly.io)
- Skip deployment and focus on local demonstration
- Create video demo instead of live deployment

**Owner**: Developer  
**Status**: Open

---

### R-9: Model Download Fails on Deployment

**Category**: Deployment  
**Probability**: Medium (if deploying)  
**Impact**: Medium  
**Priority**: **MEDIUM**

**Description**:
spaCy model download may fail during deployment build process, or model may not be included in deployment.

**Consequences**:
- Deployed application missing NLP functionality
- Build fails
- Users cannot use NLP detection

**Mitigation**:
- Include model download in `requirements.txt` or build script
- Test deployment process thoroughly
- Provide fallback to rule-based detection if model missing
- Document model requirements in deployment guide

**Contingency**:
- Pre-download model and include in repository (if license permits and size acceptable)
- Use model from Hugging Face instead of spaCy
- Deploy rule-based version only

**Owner**: Developer  
**Status**: Open

---

## Research Risks

### R-10: Synthetic Dataset Not Representative

**Category**: Research - Validity  
**Probability**: Medium  
**Impact**: Medium  
**Priority**: **MEDIUM**

**Description**:
Synthetic dataset generated with Faker may not reflect real-world PII complexity, leading to results that don't generalize.

**Consequences**:
- Research findings may not apply to real data
- Over-optimistic metrics
- Reviewers may question validity

**Mitigation**:
- Include diverse PII formats in generation
- Add adversarial examples (malformed, noisy)
- Document dataset generation methodology clearly
- Acknowledge limitation in research report
- Use Faker's localized providers for realistic data

**Contingency**:
- Clearly label results as "synthetic data evaluation"
- Discuss generalization limitations in report
- Suggest future work with real-world datasets
- Emphasize comparative nature (Method A vs. B) rather than absolute performance

**Owner**: Developer  
**Status**: Open

---

### R-11: Experiment Results Not Reproducible

**Category**: Research - Reproducibility  
**Probability**: Low  
**Impact**: High  
**Priority**: **MEDIUM**

**Description**:
Experiments may produce different results when re-run due to non-deterministic behavior or missing configuration.

**Consequences**:
- Research credibility questioned
- Cannot verify results independently
- Difficult to debug issues

**Mitigation**:
- Use fixed random seeds everywhere
- Pin all dependency versions
- Document Python version, OS, hardware
- Archive evaluation dataset
- Test reproducibility during Milestone 11
- Provide CLI scripts for re-running experiments

**Contingency**:
- If minor variations occur, report mean ± std dev
- Document sources of non-determinism
- Provide multiple run results
- Focus on qualitative insights rather than exact numbers

**Owner**: Developer  
**Status**: Open

---

## Security and Privacy Risks

### R-12: PII Leakage in Logs or Database

**Category**: Security - Privacy  
**Probability**: Medium  
**Impact**: High  
**Priority**: **HIGH**

**Description**:
Accidental logging of raw PII values or storing PII in database could expose sensitive information.

**Consequences**:
- Privacy violation
- Defeats purpose of privacy-aware system
- Security vulnerability if logs/database exposed
- Reputation damage

**Mitigation**:
- Code review all logging statements (never log PII values)
- Use PII category and count only in logs
- Audit database schema (no raw PII columns)
- Test with sample data and inspect logs/database
- Implement logging wrapper that redacts PII
- Add automated tests to check for PII in logs

**Contingency**:
- If PII found in logs, redact historical logs
- Update code immediately and re-test
- Document incident and prevention measures
- Implement pre-commit hooks to catch PII logging

**Owner**: Developer  
**Status**: Open  
**Priority**: **HIGH**

---

### R-13: CSV Formula Injection on Export

**Category**: Security - Input Validation  
**Probability**: Medium  
**Impact**: Medium  
**Priority**: **MEDIUM**

**Description**:
Exported CSV files may contain formula injection payloads (e.g., `=1+1`, `@SUM(A1:A10)`) that execute when opened in Excel.

**Consequences**:
- Security vulnerability for users opening exported files
- Potential for malicious code execution
- Professional credibility impacted

**Mitigation**:
- Implement CSV export sanitization
- Prefix dangerous characters (`=`, `+`, `-`, `@`) with single quote (`'`)
- Test with CSV files containing formula-like strings
- Document sanitization in README
- Add warning in UI about opening CSV files

**Contingency**:
- If missed initially, add in Milestone 10 (hardening)
- Provide JSON export as alternative (no formula risk)
- Document issue and mitigation in README

**Owner**: Developer  
**Status**: Open

---

### R-14: Path Traversal Vulnerability

**Category**: Security - Input Validation  
**Probability**: Low  
**Impact**: High  
**Priority**: **MEDIUM**

**Description**:
User-controlled filenames or paths could allow reading/writing files outside intended directories.

**Consequences**:
- Security vulnerability
- Potential data exposure or corruption
- System compromise (low risk for local app, but still unprofessional)

**Mitigation**:
- Use Python's `tempfile` module (generates safe paths)
- Validate filenames (reject `..`, `/`, `\`)
- Use `pathlib` for safe path operations
- Never use user-provided paths directly for file operations
- Test with malicious filenames (`../../etc/passwd`, etc.)

**Contingency**:
- Add validation in Milestone 10 if not already present
- Code review all file operations
- Add security testing to test suite

**Owner**: Developer  
**Status**: Open

---

## Project Management Risks

### R-15: Scope Creep

**Category**: Project Management  
**Probability**: Medium  
**Impact**: Medium  
**Priority**: **MEDIUM**

**Description**:
Adding features beyond initial scope (e.g., additional PII types, cloud storage, authentication) may delay completion.

**Consequences**:
- Project timeline extends beyond 12 weeks
- Core features rushed or incomplete
- Never reach "done" state

**Mitigation**:
- Strictly follow defined requirements and milestones
- Defer enhancements to "Future Work" section
- Complete MVP (Milestones 1-10) before optional features
- Regularly review scope against original requirements

**Contingency**:
- If timeline pressured, skip optional Milestone 12 (deployment)
- Focus on research quality over additional features
- Document deferred features clearly

**Owner**: Developer  
**Status**: Open

---

### R-16: Milestone Dependencies Cause Delays

**Category**: Project Management  
**Probability**: Medium  
**Impact**: Medium  
**Priority**: **MEDIUM**

**Description**:
Blocking issues in early milestones cascade and delay later milestones.

**Consequences**:
- Project timeline slips
- Rushed implementation to catch up
- Quality suffers

**Mitigation**:
- Address blocking issues immediately
- Don't proceed to next milestone with known blockers
- Maintain buffer time in estimates (8-12 weeks range)
- Seek help early if stuck

**Contingency**:
- Re-prioritize milestones if needed
- Skip optional features to stay on track
- Accept reduced scope rather than poor quality

**Owner**: Developer  
**Status**: Open

---

### R-17: Burnout or Loss of Motivation

**Category**: Project Management  
**Probability**: Low  
**Impact**: High  
**Priority**: **MEDIUM**

**Description**:
Solo development over 8-12 weeks may lead to burnout or loss of motivation.

**Consequences**:
- Project abandoned or incomplete
- Poor quality due to rushed work
- Missed master's application deadline

**Mitigation**:
- Work in sustainable increments (don't overwork)
- Celebrate milestone completions
- Take breaks between milestones
- Keep end goal (master's application) visible
- Reach out for support if struggling

**Contingency**:
- Reduce scope if necessary to finish core features
- Extend timeline if possible
- Prioritize quality over completeness

**Owner**: Developer  
**Status**: Open

---

## Documentation Risks

### R-18: Documentation Becomes Outdated

**Category**: Documentation  
**Probability**: High  
**Impact**: Low  
**Priority**: **MEDIUM**

**Description**:
Code changes during implementation may not be reflected in documentation, leading to inaccurate guides.

**Consequences**:
- Setup instructions don't work
- Users confused by incorrect documentation
- Wasted time troubleshooting

**Mitigation**:
- Update README and docs immediately when making breaking changes
- Test setup instructions on clean environment (Milestone 12)
- Review documentation during each milestone completion
- Use inline code comments to stay synchronized

**Contingency**:
- Dedicate time in Milestone 11 to review and update all documentation
- Test fresh installation to catch documentation errors
- Fix immediately if discovered

**Owner**: Developer  
**Status**: Open

---

### R-19: Missing or Incomplete Research Report

**Category**: Documentation - Research  
**Probability**: Low  
**Impact**: High  
**Priority**: **HIGH**

**Description**:
Research report may be rushed or incomplete, weakening master's application.

**Consequences**:
- Poor impression on admission committee
- Application rejected
- Wasted effort on implementation without good documentation

**Mitigation**:
- Allocate sufficient time for Milestone 11 (1-2 weeks)
- Write report sections incrementally during implementation
- Prioritize research report over optional deployment
- Review report with mentor or peer before finalizing

**Contingency**:
- Extend Milestone 11 if needed (delay deployment)
- Use planning documents as basis for report methodology section
- Focus on clear presentation of results over perfect prose

**Owner**: Developer  
**Status**: Open  
**Priority**: **HIGH**

---

## Risk Summary by Priority

### Critical Risks (Immediate Attention)
- **R-1**: NLP Model Compatibility Issues on Windows
  - *Action*: Test spaCy installation in Milestone 1

### High Priority Risks
- **R-2**: Presidio Version Compatibility with Python 3.11
  - *Action*: Test Presidio installation in Milestone 1
- **R-12**: PII Leakage in Logs or Database
  - *Action*: Code review all logging, add tests
- **R-19**: Missing or Incomplete Research Report
  - *Action*: Allocate sufficient time, don't rush

### Medium Priority Risks
- **R-3**: DuckDB File Locking
- **R-4**: Memory Consumption
- **R-5**: Performance Degradation
- **R-6**: False Positive Rate
- **R-7**: False Negative Rate
- **R-8**: Streamlit Cloud Limitations
- **R-9**: Model Download Fails on Deployment
- **R-10**: Synthetic Dataset Not Representative
- **R-11**: Experiment Results Not Reproducible
- **R-13**: CSV Formula Injection
- **R-14**: Path Traversal Vulnerability
- **R-15**: Scope Creep
- **R-16**: Milestone Dependencies
- **R-17**: Burnout
- **R-18**: Documentation Outdated

---

## Risk Monitoring Plan

### Weekly Review
- Review open risks
- Update probability/impact if new information available
- Check mitigation progress
- Escalate if mitigation not working

### Milestone Checkpoints
- Verify milestone-specific risks addressed
- Document any new risks discovered
- Update risk register
- Adjust subsequent milestones if needed

### Final Review (Milestone 11)
- Review all risks and outcomes
- Document lessons learned
- Include risk management discussion in research report (if relevant)

---

**Document Status**: Draft  
**Review Frequency**: Weekly during implementation  
**Next Review**: After Milestone 1 completion  
**Owner**: Project Developer
