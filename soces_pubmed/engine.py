import sys
import os

# Add the Laya submodule to the path so we can import it without pip installing
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYA_DIR = os.path.join(ROOT_DIR, "laya")
if LAYA_DIR not in sys.path:
    sys.path.insert(0, LAYA_DIR)

from laya.common import build_model
from transformers import AutoTokenizer

from soces_pubmed.config import DEFAULT_CONFIG, BASE_ENCODER

def initialize_untrained_model():
    """
    Initializes a fresh Laya DecisionModel using the BioClinical-ModernBERT-large
    encoder. This is the first step before training custom decision heads.
    """
    print(f"Initializing untrained DecisionModel with config: {DEFAULT_CONFIG}")
    # build_model uses AutoModel.from_pretrained under the hood when no local dir is found.
    model = build_model(DEFAULT_CONFIG)
    return model

def load_tokenizer():
    """Loads the tokenizer for the base encoder to ensure alignment."""
    print(f"Loading tokenizer for {BASE_ENCODER}")
    return AutoTokenizer.from_pretrained(BASE_ENCODER)
