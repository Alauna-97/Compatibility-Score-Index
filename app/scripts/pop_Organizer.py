import mysql.connector
import random
from faker import Faker

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="csi"
)

fake = Faker()
mycursor = mydb.cursor()


def populateOrg(records):
    for i in range(16, records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = first_name
        email = username + last_name + "@yahoo.com"
        password = "1100"

        sql = "INSERT INTO User (user_id, type, first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (i, "Organizer", first_name,
               last_name, username, email, password)

        mycursor.execute(sql, val)
        mydb.commit()

        position = random.choice(
            ['Secretary', 'CEO', 'Treasurer', 'Vice President', 'Supervisor', 'Manager'])

        sql = "INSERT INTO Organizer (user_id, position) VALUES (%s, %s)"
        val = (mycursor.lastrowid, position)

        mycursor.execute(sql, val)
        mydb.commit()


if __name__ == '__main__':
    populateOrg(21)
    print("Organizers Added!")
