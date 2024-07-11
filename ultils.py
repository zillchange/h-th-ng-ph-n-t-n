import base64
file_path_default = "MacBook.jpg"

class Settings:
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 180  # in mins
    COOKIE_NAME = "access_token"
settings = Settings()

def encode_id(id: int) -> str:
    encoded_id = base64.urlsafe_b64encode(str(id).encode()).decode()
    return encoded_id

def decode_id(encoded_id: str) -> int:
    decoded_id = base64.urlsafe_b64decode(encoded_id).decode()
    return int(decoded_id)