

# Function to create a JWT token
def create_jwt_token(user_id: str):
    expiration = datetime.now() + timedelta(hours=1)
    payload = {"sub": user_id, "exp": expiration}
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token