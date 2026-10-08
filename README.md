# soces-pubmed

**soces-pubmed** is a specialized, highly calibrated System-1 decision model built for PubMed and clinical text. It adapts the [Laya](https://github.com/NandhaKishorM/laya) (Fast System-1 decision engine) framework and utilizes the `thomas-sounack/BioClinical-ModernBERT-large` model as its underlying encoder.

## Objective

The goal of this project is to create a robust, high-performance inference engine capable of making rapid clinical decisions, triage routing, and guardrail checks on biomedical text. 

By leveraging the Laya framework's calibrated probability engine and swapping the base encoder for a domain-specific biomedical ModernBERT, `soces-pubmed` achieves accurate, lightning-fast predictions on clinical datasets.

## Framework & Architecture

- **Core Engine**: Built using components adapted from the `laya` framework. The Laya submodule is retained in this repository strictly as a reference implementation.
- **Base Encoder**: `thomas-sounack/BioClinical-ModernBERT-large`.
- **Implementation Strategy**: Custom biomedical logic (presets, configuration, engine wrappers, and training scripts) is built directly in the root directory, cleanly separated from the unmodified `laya` reference source.

## Directory Structure

```text
soces-pubmed/
├── .gitmodules             # Existing submodule pointer
├── laya/                   # Unmodified Laya reference submodule
├── pyproject.toml          # Custom dependencies (torch, transformers, etc.)
├── data/                   # Biomedical JSONL training datasets (Source does not allow redistribution, .gitignored)
├── models/                 # Trained BioClinical decision model checkpoints (.gitignored)
└── soces_pubmed/           # Main application package
    ├── __init__.py
    ├── config.py           # Sets thomas-sounack/BioClinical-ModernBERT-large as base
    ├── engine.py           # Core decision engine logic adapted from laya/common.py
    ├── presets.py          # Clinical routing, acuity, and PHI schemas
    ├── train.py            # Training logic adapted from laya/train.py
    └── serve.py            # Fast HTTP API for the clinical models
```

## Datasets & Licensing

The training datasets for this project are derived directly from **PubMed abstracts** and clinical literature. 

**Important Data Licensing & Contribution Notice:**
- **Raw Data**: While PubMed Central (PMC) has an Open Access subset that permits redistribution, a vast majority of MEDLINE abstracts and full-text articles remain under strict publisher copyright. Because this project relies on data where the source prohibits redistribution, all raw `.jsonl` datasets in the `data/` directory remain strictly internal and `.gitignored`.
- **Model Weights**: Training a model on copyrighted text is generally protected under Text and Data Mining (TDM) exceptions or Fair Use (depending on jurisdiction), meaning the resulting trained model weights (decision heads) can typically be distributed. 
- **PHI / Privacy**: To comply with privacy standards, final model releases are strictly audited to ensure no Protected Health Information (PHI) or verbatim copyrighted text is memorized or emitted.
