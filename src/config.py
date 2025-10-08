import os

from dotenv import load_dotenv

load_dotenv()


####################################################################
## Various environment variables as credentials for
## programmatic access.
##
## This class can read those environment variables, verify
## they exist, and return them.
####################################################################
class Config:
    def verify(self):
        errors = ""
        if os.environ.get("FRED_API_TOKEN", "") == "":
            errors += "The environment variable: FRED_API_TOKEN is not set."
            return errors, False
        return errors, True

    def get_fred_key(self):
        return os.environ.get("FRED_API_TOKEN", "")
