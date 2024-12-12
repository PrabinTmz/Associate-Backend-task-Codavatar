import requests
from faker import Faker
import random

# Base URL for the FastAPI server
BASE_URL = "http://localhost:8000/api/v1"

# Login endpoint to authenticate and retrieve JWT
LOGIN_ENDPOINT = BASE_URL + "/auth/token"

# API endpoints
AUTH_ENDPOINT = BASE_URL + "/auth"


USER_CREDENTIALS = {"email": "johndoegm@gmail.com", "password": "hello_world"}


fake = Faker()


def register_user(user_data):
    response = requests.post(f"{AUTH_ENDPOINT}/register", json=user_data)

    if response.status_code == 200:
        print(f"User created: {user_data}")
    else:
        print(f"Failed to create user: {user_data}")
        print(response.json())


def authenticate():
    """
    Authenticate using credentials and get JWT token.
    """
    print("Authenticating...")
    response = requests.post(LOGIN_ENDPOINT, json=USER_CREDENTIALS)

    if response.status_code == 200:
        token = response.json().get("access_token")
        print("Authentication successful. Token received.")
        return token
    else:
        print("Authentication failed.")
        print(response.json())
        return None


def generate_phone_number():
    """Generate a realistic random phone number."""
    # International prefix range examples
    # country_codes = ["+1", "+44", "+33", "+91", "+81", "+61", "+49"]
    # country_code = random.choice(country_codes)  # Pick a random international code
    number = "".join(
        [str(random.randint(0, 9)) for _ in range(7)]
    )  # Generate 8 random digits
    return f"+91 974{number}"


def populate_records(token, num, data={}, url=""):
    """
    Populate a random number of users using random data.
    """

    headers = {"Authorization": f"Bearer {token}"}

    # print(f"Populating {num} random numbers...")
    count = 0
    for _ in range(num):
        data = {"number": generate_phone_number()}

        response = requests.post(url=url, json=data, headers=headers)
        if not response.status_code == 201:
            print(response.json())
            continue
        else:
            count += 1
            print(count, response.json())

    print(f"{count} records created")


def get_data(token, url):
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url=url, headers=headers)
    print(response.json())


def main():
    register_user(USER_CREDENTIALS)

    # Authenticate and get JWT token
    token = authenticate()
    if not token:
        return

    # Generate a random number of users to populate
    url = f"{BASE_URL}/phonenumbers?limit=25&offset=55"

    # populate_records(token=token, num=2000, url=url)

    get_data(token, url)


if __name__ == "__main__":
    main()
