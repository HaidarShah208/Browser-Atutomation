from faker import Faker

fake = Faker()

def generate_user():
    return {
        "fullName": fake.name(),
        "email": fake.email(),
        "phoneNumber": fake.msisdn()[:11],
        "password": "Test@12345"
    }