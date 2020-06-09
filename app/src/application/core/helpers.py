import uuid


def generate_uuid():
    return str(uuid.uuid4())


def is_valid_uuid(uuid_to_test):
    try:
        uuid.UUID(str(uuid_to_test))
        return True
    except ValueError:
        return False
