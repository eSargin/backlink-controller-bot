import jwt

jwtSecretKey = "secretkey"


def CheckIsAuthenticated(token):
    if token is None or token == "" or token == "null" or token == "undefined":
        return False
    # decode jwt token
    try:
        decoded = jwt.decode(token, jwtSecretKey, algorithms=["HS256"])
        if decoded is None:
            return False
    except Exception as e:
        return False

    if decoded is None:
        return False
    return True


def EncodeToken(token):
    print("Token -> ", token)
    decoded = jwt.decode(token, jwtSecretKey, algorithms=["HS256"])
    return decoded
