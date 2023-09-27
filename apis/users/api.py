# Python
import re

# Django
from django.contrib.auth.hashers import make_password

# Ojitos369
from ojitos369.utils import get_unique_key

# User
from .mails import CorreoActivacion
from app.core.bases.apis import PostApi, GetApi, get_d, pln

class CreateUser(PostApi):
    def main(self):
        pln("CreateUser")
        
        username = get_d(self.data, "username")
        username = username.strip()
        regex_username = re.compile('^[a-zA-Z0-9_]+$')
        if not regex_username.match(username):
            raise self.MYE("Username invalido, solo se permiten letras, numeros y _")
        
        lower_username = username.lower()
        password = get_d(self.data, "password")
        password = make_password(password)
        email = get_d(self.data, "email")
        email = email.lower().strip()
        regex_email = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not regex_email.match(email):
            raise self.MYE("Email invalido")

        phone = get_d(self.data, "phone", default=None)
        if phone:
            phone = phone.lower().strip().replace(" ", "").replace("-", "")
        regex_phone = re.compile('^\+?[0-9]+$')
        if phone and not regex_phone.match(phone):
            raise self.MYE("Telefono invalido")

        name = get_d(self.data, "name", default=None)
        lastname = get_d(self.data, "lastname", default=None)
        birthdate = get_d(self.data, "birthdate", default=None)
        if birthdate:
            birthdate = self.str_to_date(birthdate)
        
        
        query = """select id_user 
                    from users 
                    where lower_username = %s
                    or email = %s
                    or phone = %s
                    """
        query_data = (lower_username, email, phone)
        rs = self.conexion.consulta_asociativa(query, query_data)
        if rs:
            raise self.MYE("User already exists")
    
        query = """insert into users
                (username, lower_username, password, email, phone, name, lastname, birthdate)
                values
                (%s, %s, %s, %s, %s, %s, %s, %s)
                """
        query_data = (username, lower_username, password, email, phone, name, lastname, birthdate)
        if not (self.conexion.ejecutar(query, query_data)):
            self.conexion.rollback()
            raise self.MYE("Error al insertar")
        self.conexion.commit()
        
        # get user_id 
        query = """select id_user 
                    from users 
                    where lower_username = %s
                    and email = %s
                    and phone = %s
                    """
        query_data = (lower_username, email, phone)
        rs = self.conexion.consulta_asociativa(query, query_data)
        id_user = rs[0]["id_user"]
        
        token = get_unique_key()
        
        query = """insert into activation_codes
                (code, user_id)
                values
                (%s, %s)
                """
        query_data = (token, id_user)

        if not (self.conexion.ejecutar(query, query_data)):
            self.conexion.rollback()
            raise self.MYE("Error al insertar")
        self.conexion.commit()

        text = f"""El codigo de activacion de tu cuenta es:\n{token}"""
        mail = CorreoActivacion({"email_text": text})
        mail.send()

        self.response = {
            "message": "User Created"
        }


