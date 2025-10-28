import os
from dotenv import load_dotenv

load_dotenv()

# Choose environment: dev / stage / prod
ENV = os.getenv("ENV", "dev")

BASES = {
    "dev": {
        "jsonplaceholder": "https://jsonplaceholder.typicode.com",
        "reqres": "https://reqres.in/api",
        "httpbin": "https://httpbin.org",
        "gorest": "https://gorest.co.in/public/v2",
    },
    # You can later add stage/prod URLs here if needed
}

def get_base_url(service_name: str):
    return BASES.get(ENV, BASES["dev"]).get(service_name)
