class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host":"localhost",
            "user":"wouter",
            "passwd":"wouter",
            "db":"dbproject1"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    def invoegen_data_charts(self):
        # Query zonder parameters
        sqlQuery = "SELECT Lichtsensor, Tijdstip FROM tblmetingen ORDER BY Tijdstip DESC limit 20;"
        self.__cursor.execute(sqlQuery)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def gebruikerToevoegen(self,email,naam,password):
        q = "INSERT INTO tblgegevens(Gebruiksnaam,Email,Wachtwoord) VALUES ('" + naam + "','" + email + "','" + password + "' )"
        self.__cursor.execute(q)
        self.__connection.commit()
        self.__cursor.close()

    def naamcontroleren(self,naam):
        q="SELECT COUNT(*) FROM tblgegevens WHERE Gebruiksnaam ='" + naam+ "';"
        self.__cursor.execute(q)
        aantal = self.__cursor.fetchone()
        self.__cursor.close()
        return aantal


    def login_controleren(self,naam):
        q="SELECT Wachtwoord FROM tblgegevens WHERE Gebruiksnaam = '" + naam + "';"
        self.__cursor.execute(q)
        result = self.__cursor.fetchone()
        self.__cursor.close()
        return result

    def test_login(self,naam):
        q = "SELECT COUNT(*) FROM tblgegevens WHERE Gebruiksnaam = '" + naam + "';"
        self.__cursor.execute(q)
        result = self.__cursor.fetchone()
        self.__cursor.close()

    def invoegen_bericht(self,naam,email,bericht):
        q = "INSERT INTO tblcontact(Naam,Email,Bericht) VALUES ('" + naam + "','" + email + "','" + bericht + "' )"
        self.__cursor.execute(q)
        self.__connection.commit()
        self.__cursor.close()