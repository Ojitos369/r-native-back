# Python
import os
import uuid
import json

# Django
from django.contrib.auth.hashers import make_password

# Ojitos369
from ojitos369.utils import generate_token

# User
from app.core.bases.apis import PostApi, GetApi, get_d, pln

class Version(GetApi):
    def main(self):
        pln("Version")
        self.response = {
            "version": "v.2309.2701",
            "cambios": [
                "Creacion de usuarios",
            ]
        }
    
    def validate_session(self):
        pass