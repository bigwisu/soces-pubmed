# soces-pubmed

**soces-pubmed** is a decision model for PubMed and clinical text. It uses the [Laya](https://github.com/NandhaKishorM/laya) framework. It uses the `thomas-sounack/BioClinical-ModernBERT-large` model as its encoder.

## Objective

This project makes a fast inference engine. The engine makes clinical decisions. It routes text. It does safety checks on medical text.

The project uses the Laya probability engine. It uses a medical ModernBERT encoder. `soces-pubmed` makes fast and accurate predictions on medical data.

## Framework and Architecture

- **Core Engine**: The engine uses parts from the `laya` framework. The Laya submodule is in this repository for reference only.
- **Base Encoder**: `thomas-sounack/BioClinical-ModernBERT-large`.
- **Implementation Strategy**: We put the medical logic in the root directory. This logic includes presets, configuration, wrappers, and training scripts. We keep this logic separate from the `laya` source code.

## Directory Structure

```text
soces-pubmed/
├── .gitmodules             # Submodule pointer
├── laya/                   # Laya reference submodule (do not change)
├── pyproject.toml          # Custom dependencies (torch, transformers)
├── data/                   # Medical JSONL training data (do not distribute)
├── models/                 # Trained model files
└── soces_pubmed/           # Main application package
    ├── __init__.py
    ├── config.py           # Sets the base model
    ├── engine.py           # Core decision engine logic
    ├── presets.py          # Clinical schemas
    ├── train.py            # Training logic
    └── serve.py            # HTTP API for the models
```

## Datasets and Licensing

The training data for this project comes from PubMed abstracts and clinical literature.

**Data Licensing and Contribution Notice:**
- **Raw Data**: Some data is Open Access. But, many MEDLINE abstracts and articles have publisher copyright. The source does not permit data distribution. We keep all raw `.jsonl` data in the `data/` directory internal. We do not commit this data to git.
- **Model Weights**: We train the model on copyrighted text. This training is usually legal under Text and Data Mining (TDM) rules or Fair Use. We can distribute the trained model weights.
- **Privacy**: We check the final models carefully. We make sure the models do not contain Protected Health Information (PHI). We make sure the models do not show exact copyrighted text.
