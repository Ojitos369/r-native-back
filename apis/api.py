# Python
import os
import uuid
import json

# User
from app.core.bases.apis import PostApi, GetApi, get_d, pln


class HelloWorld(GetApi):
    def main(self):
        self.response = {
            'message': 'Hello World'
        }


class Test(GetApi):
    def main(self):
        pln("Test")
        
        name = uuid.uuid4()
        
        query = f"""insert into test
                    (name) values ("{name}")
                    """
        
        if not (self.conexion.ejecutar(query)):
            self.conexion.rollback()
            raise self.MYE("Error al insertar")
        
        query = f"""select max(id) as id from test"""
        
        r = self.conexion.consulta_asociativa(query)
        id = None
        if r:
            id = get_d(r[0], 'id')
        
        self.conexion.commit()
        
        self.response = {
            "message": f"Test Added: {id}"
        }
        
