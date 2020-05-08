import mysql.connector
import random
from faker import Faker

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="csi2"
)

fake = Faker()
mycursor = mydb.cursor()


def populateReg(records):
    for i in range(1, records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = first_name
        email = last_name + username + "@gmail.com"
        password = "1234"

        sql = "INSERT INTO User (user_id, type, first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (i, "Regular", first_name, last_name, username, email, password)

        mycursor.execute(sql, val)
        mydb.commit()

        gender = random.choice(
            ['Female', 'Male'])

        height = random.randint(142, 198)
        age = random.randint(22, 35)
        leadership = random.choice(
            ['Autocratic', 'Laissez-Faire', 'Democratic'])
        hobby = random.choice(
            ['Sports', 'Music', 'Exercising', 'Shopping', 'Dancing', 'Watching TV', 'Reading and Writing', 'Arts'])
        ethnicity = random.choice(
            ['Black', 'White', 'Chinese', 'Indian', 'Hispanic'])
        occupation = random.choice(
            ['Business', 'Science', 'Technology', 'Construction', 'Communication', 'Law'])
        education = random.choice(
            ['Bachelors', 'Masters', 'PhD', 'Diploma', 'Associate Degree'])
        personality = random.choice(['Introvert', 'Extrovert', 'Ambivert'])

        sql = "INSERT INTO Regular (user_id, gender, age, height, leadership, ethnicity, personality, education, hobby, occupation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (mycursor.lastrowid, gender, age,
               height, leadership, ethnicity, personality, education, hobby, occupation)

        mycursor.execute(sql, val)
        mydb.commit()


if __name__ == '__main__':
    populateReg(16)
    print("Regular Users Added!")
