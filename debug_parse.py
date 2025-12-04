import types
import sys

# Inject a fake 'ollama' module so we don't need the real dependency for parsing tests
fake_ollama = types.ModuleType('ollama')
fake_ollama.chat = lambda model, messages: {'message': {'content': ''}}
sys.modules['ollama'] = fake_ollama

from verifier import verify_content_with_image

# Monkeypatch verifier.ollama.chat in the module
import verifier

samples = [
    # Standard formatted response
    "PERCENTAGE: 30\nERRORS: Claims Earth is flat (scientifically proven spherical), States vaccines cause autism (debunked by medical research)\nANALYSIS: The text contains multiple false claims contradicting scientific evidence.",

    # JSON-like response
    '{"percentage": 85, "errors": "none", "analysis": "Mostly accurate with small issues."}',

    # Malformed but contains percentage
    "This is a report. PERCENTAGE: 45. Some other text. ERRORS: Misstates climate science. ANALYSIS: Needs corrections.",

    # No percentage present
    "ERRORS: Unsupported claim\nANALYSIS: No numeric score provided by model.",
]

for i, sample in enumerate(samples, 1):
    # Replace ollama.chat to return sample
    verifier.ollama.chat = lambda model, messages: {'message': {'content': sample}}
    res = verify_content_with_image(text="dummy text to verify")
    print(f"--- Sample {i} ---")
    print(res)
    print()
