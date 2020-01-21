import bcrypt


def generate_bcrypt_hash(raw_password):
    """
    generates the encrypted hash
    :param raw_password:
    :return: The Bcrypt hash
    """
    result = bcrypt.hashpw(str(raw_password).encode("utf-8"), bcrypt.gensalt())
    return result.decode("utf-8")
