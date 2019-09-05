#!.env/bin/python
import os

from app import api

if __name__ == "__main__":
    api.run(
        host="0.0.0.0",
        port=5580,
        debug=True
    )
