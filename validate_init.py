import sys
import os

from soces_pubmed.engine import initialize_untrained_model, load_tokenizer

def run_validation():
    print("--- Phase 2: Tokenizer Alignment ---")
    try:
        tokenizer = load_tokenizer()
        print("Success! Tokenizer loaded properly.")
    except Exception as e:
        print(f"Failed to load tokenizer: {e}")
        sys.exit(1)

    print("\n--- Phase 2: Model Initialization ---")
    try:
        model = initialize_untrained_model()
        print("Success! DecisionModel initialized with the BioClinical encoder weights.")
        print(f"Model class: {model.__class__.__name__}")
        print(f"Encoder class: {model.encoder.__class__.__name__}")
    except Exception as e:
        print(f"Failed to initialize model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_validation()
