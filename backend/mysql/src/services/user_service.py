class UserService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_user(self, dni):
        query = "INSERT INTO users (dni) VALUES (%s)"
        values = (dni,)
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(query, values)
            self.db_connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.db_connection.rollback()
            raise e
        finally:
            cursor.close()
    
    def add_test_results(self, dni, result_dict):
        query = """
            INSERT INTO resultados_test
            (dni, `Sangre`, `Bilirruina`, `Urobilinogeno`, `Cuerpos cetonicos`,
             `Glucosa`, `Proteina`, `Nitrito`, `Leucocitos`, `pH`, `Densidad relativa`)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        print(result_dict, "DENTRO DEL AGREGADO EN LOS RESULTADOOOOOOOOOOSSSOOSOSO")
        vals = (
            dni,
            result_dict.get('Sangre'),
            result_dict.get('Bilirruina'),
            result_dict.get('Urobilinogeno'),
            result_dict.get('Cuerpos cetonicos'),
            result_dict.get('Glucosa'),
            result_dict.get('Proteina'),
            result_dict.get('Nitrito'),
            result_dict.get('Leucocitos'),
            result_dict.get('pH'),
            result_dict.get('Densidad relativa')
        )
        cur = self.db_connection.cursor()
        try:
            cur.execute(query, vals)
            self.db_connection.commit()
            return cur.lastrowid
        except Exception as e:
            self.db_connection.rollback()
            raise e
        finally:
            cur.close()
    
    def get_all_users(self):
        query = "SELECT id, dni FROM users ORDER BY id DESC"
        cursor = self.db_connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def get_test_results_by_dni(self, dni):
        query = """
            SELECT id, dni, `Sangre`, `Bilirruina`, `Urobilinogeno`, `Cuerpos cetonicos`,
                   `Glucosa`, `Proteina`, `Nitrito`, `Leucocitos`, `pH`, `Densidad relativa`, created_at
            FROM resultados_test
            WHERE dni = %s
            ORDER BY id DESC
        """
        cursor = self.db_connection.cursor(dictionary=True)
        try:
            cursor.execute(query, (dni,))
            return cursor.fetchall()
        finally:
            cursor.close()