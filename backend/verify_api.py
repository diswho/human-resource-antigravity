import requests
import json

base_url = "http://localhost/api/v1"

# Login to get token
login_data = {
    "username": "admin@example.com",
    "password": "changethis"
}
try:
    response = requests.post(f"{base_url}/login/access-token", data=login_data)
    response.raise_for_status()
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get employees
    response = requests.get(f"{base_url}/employees", headers=headers)
    response.raise_for_status()
    data = response.json()
    print(f"Total employees: {data['count']}")
    if data['data']:
        print(f"Debug - First employee keys: {data['data'][0].keys()}")
        print(f"Debug - First employee email: {data['data'][0].get('email')}")

    print("\nFirst 5 employees with email:")
    for emp in data['data'][:5]:
        print(
            f"- {emp['emp_pin']}: {emp['firstname']} {emp['lastname']} ({emp.get('email')})")

    emails_found = any(e.get('email') for e in data['data'])
    if emails_found:
        print("\nSUCCESS: Found email data in the response!")
    else:
        print("\nWARNING: No email data found. Ensure users are linked to employees.")

except Exception as e:
    print(f"Error: {e}")
