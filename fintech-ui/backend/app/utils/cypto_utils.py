import hashlib
import hmac

def generate_hmac_signature(secret_key: str, message: str) -> str:
    return hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()

def verify_hmac_signature(secret_key: str, message: str, signature: str) -> bool:
    return hmac.compare_digest(generate_hmac_signature(secret_key, message), signature)