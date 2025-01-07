import jwt
from datetime import datetime, timedelta

# the chainlit auth environment variable
CHAINLIT_AUTH_SECRET = "KO:3xIBhghKtiShvJv@vEDCxAP.BPy4b$LN:Hm,Gxo>mL5mo5Q@Ltgq6%yTLkF5_"


# the function to create jwt auth for chainlit copilot
def create_jwt(identifier: str, metadata: dict) -> str:
    to_encode = {
      "identifier": identifier,
      "metadata": metadata,
      "exp": datetime.utcnow() + timedelta(minutes=60 * 24 * 15),  # 15days
      }

    encoded_jwt = jwt.encode(to_encode, CHAINLIT_AUTH_SECRET, algorithm="HS256")
    return encoded_jwt


# access_token = create_jwt(identifier="vUWSJREpJy")
# print(access_token)
