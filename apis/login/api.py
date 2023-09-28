# Python
import os
import uuid
import json

# Django
from django.contrib.auth.hashers import check_password

# Ojitos369
from ojitos369.utils import get_unique_key

# User
from app.core.bases.apis import PostApi, GetApi, get_d, pln

class Login(PostApi):
    def main(self):
        pln("Login")

        username = get_d(self.data, "username")
        username = username.lower().strip()
        password = get_d(self.data, "password")
        
        # pln(f"username: {username}")
        # pln(f"password: {password}")
        
        query = """select *
                    from users
                    where (lower_username = %s
                    or email = %s)
                    and active = 1
                    """
        query_data = (username, username)
        rs = self.conexion.consulta_asociativa(query, query_data)

        if not rs:
            raise self.MYE("Revise las credenciales de acceso")
        user = rs[0]
        if not check_password(password, user["password"]):
            raise self.MYE("Revise las credenciales de acceso")
        
        token = get_unique_key()
        
        query = """update users
                    set last_login = now(),
                    where id_user = %s
                    """
        query_data = (user["id_user"],)
        if not (self.conexion.ejecutar(query, query_data)):
            self.conexion.rollback()
            raise self.MYE("Error al actualizar")
        self.conexion.commit()
        
        user = {
            "username": user["username"],
            "email": user["email"],
            "phone": user["phone"],
            "status": user["status"],
            "validated": user["validated"],
            "active": user["active"],
            "name": user["name"],
            "lastname": user["lastname"],
            "birthdate": user["birthdate"],
        }

        self.status = {
            "message": "Login exitoso",
            "token": token,
            "user": user,
        }

    def validate_session(self):
        pass