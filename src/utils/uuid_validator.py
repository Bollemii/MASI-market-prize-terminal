from uuid import UUID


def uuid_validator(uuid_string):
    try:
        UUID(uuid_string, version=4)
    except ValueError:
        return False
    return True
