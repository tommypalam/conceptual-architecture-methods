"""Verify the short-ID continuation using the same zero-network archive audit."""
import json
from verify_phase3_recognition_recovery import checkpoint
from phase3_recognition_transport import TRANSPORT, PREVIOUS, collect

if __name__ == "__main__":
    print(json.dumps(checkpoint(TRANSPORT, PREVIOUS, collect,
                               "phase3_recognition_transport_r1_20260913.zip")))
