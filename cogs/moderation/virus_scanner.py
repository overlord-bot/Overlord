import os

from dotenv import load_dotenv
import vt

vt_token = os.getenv(load_dotenv("VT_TOKEN"))
client = vt.Client(vt_token)

