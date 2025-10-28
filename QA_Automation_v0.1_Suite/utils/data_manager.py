import random
import string

def random_name(prefix="User"):
    return f"{prefix}_{''.join(random.choices(string.ascii_letters, k=5))}"

def random_email():
    return f"{''.join(random.choices(string.ascii_lowercase, k=6))}@example.com"

def cleanup_test_data(api_client, resource_path):
    try:
        api_client.delete(resource_path)
    except Exception as e:
        print(f"Cleanup failed: {e}")
