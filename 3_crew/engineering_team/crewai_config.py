import os
import time
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Rate limiting configuration
RATE_LIMIT_DELAY = 2  # seconds between requests
last_request_time = 0

def rate_limit(func):
    """Decorator to add rate limiting between API calls"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        global last_request_time
        current_time = time.time()
        time_since_last = current_time - last_request_time
        
        if time_since_last < RATE_LIMIT_DELAY:
            sleep_time = RATE_LIMIT_DELAY - time_since_last
            print(f"Rate limiting: waiting {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)
        
        last_request_time = time.time()
        return func(*args, **kwargs)
    return wrapper

# LiteLLM configuration for Anthropic
LITELLM_CONFIG = {
    "model": "anthropic/claude-3-5-sonnet-20241022",
    "api_key": os.getenv("ANTHROPIC_API_KEY"),
    "max_tokens": int(os.getenv("ANTHROPIC_MAX_TOKENS", 4000)),
    "temperature": float(os.getenv("ANTHROPIC_TEMPERATURE", 0.7)),
    "timeout": int(os.getenv("LITELLM_REQUEST_TIMEOUT", 180)),
    "max_retries": int(os.getenv("LITELLM_MAX_RETRIES", 3)),
    "retry_delay": int(os.getenv("LITELLM_RETRY_DELAY", 5)),
}

# Print configuration on import
print("🔧 CrewAI Configuration Loaded:")
print(f"   Model: {LITELLM_CONFIG['model']}")
print(f"   Max Tokens: {LITELLM_CONFIG['max_tokens']}")
print(f"   Temperature: {LITELLM_CONFIG['temperature']}")
print(f"   Rate Limit Delay: {RATE_LIMIT_DELAY}s")
print(f"   Timeout: {LITELLM_CONFIG['timeout']}s")

