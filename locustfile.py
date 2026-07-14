import random
import string
import logging
from locust import HttpUser, task, between

# Ye setup terminal aur Locust UI k "LOGS" tab dono me print karwayega
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def random_string(length=8):
    """Random string generate karne k liye - taake har user ka unique email/name bane"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


class SignupUser(HttpUser):
    # Har request k darmiyan 1 se 3 second ka random wait (real user jaisa behavior)
    wait_time = between(1, 3)

    @task
    def signup(self):
        # Har call pe unique data generate hoga taake API "user already exists" na de
        unique_id = random_string()
        name = f"testuser_{unique_id}"
        email = f"testuser_{unique_id}@example.com"

        payload = {
            "name": name,
            "email": email,
            "password": "TestPass123!"
        }

        with self.client.post(
            "https://www.champzones.com/api/signup",
            json=payload,
            catch_response=True,
            name="POST /signup"
        ) as response:
            if response.status_code in (200, 201):
                response.success()
                # Yahan print ho jayega konsa user successfully create hua
                logger.info(f"[SIGNUP OK] name={name} email={email} status={response.status_code}")
            else:
                response.failure(
                    f"Signup failed: status={response.status_code}, body={response.text[:200]}"
                )
                logger.info(f"[SIGNUP FAIL] name={name} email={email} status={response.status_code}")