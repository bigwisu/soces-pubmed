"""
Configuration defaults for soces-pubmed.
Hardcodes the base encoder to the specialized biomedical model.
"""

# Base encoder for all clinical decision tasks
BASE_ENCODER = "thomas-sounack/BioClinical-ModernBERT-large"

# Default configuration template passed into the decision engine
DEFAULT_CONFIG = {
    "encoder": BASE_ENCODER,
    "head_layers": 2,
    "head_max_len": 256,
}
