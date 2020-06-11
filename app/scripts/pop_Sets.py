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


def populateSet(records):

    # # creating an admin
    # sql = "INSERT INTO User (user_id, type, first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # val = (1, "Administrator", "", "","admin", "csi@gmail.com", "pass")

    # mycursor.execute(sql, val)
    # mydb.commit()

    # # creating a new organizer
    # sql = "INSERT INTO User (user_id, type, first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # val = (2, "Organizer", "Carl", "Beckford",
    #        "Carl", "carl.beckford@yahoo.com", "1100")

    # mycursor.execute(sql, val)
    # mydb.commit()

    # position = random.choice(
    #     ['Secretary', 'CEO', 'Treasurer', 'Vice President', 'Supervisor', 'Manager'])

    # sql = "INSERT INTO Organizer (user_id, position) VALUES (%s, %s)"
    # val = (mycursor.lastrowid, position)

    # mycursor.execute(sql, val)
    # mydb.commit()

    # # creating one set
    # sql = "INSERT INTO Sets (sid, set_name, purpose, code, organizer) VALUES (%s, %s, %s, %s, %s)"
    # val = (1, "Maths", "Teach maths", "XU38JSUFK", 2)

    # mycursor.execute(sql, val)
    # mydb.commit()

    # # Lanai
    # sql = "INSERT INTO User (user_id, type, first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # val = (3, "Regular", "Lanai", "Nevers",
    #        "Lanai", "lanai@yahoo.com", "pass")

    # mycursor.execute(sql, val)
    # mydb.commit()

    # sex = random.choice(
    #     ['Female', 'Male'])

    # pref_sex = random.choice(
    #     ['Female', 'Male'])

    # height = random.randint(142, 198)
    # age = random.randint(22, 35)
    # leadership = random.choice(
    #     ['Autocratic', 'Laissez-Faire', 'Democratic'])
    # hobby = random.choice(
    #     ['Sports', 'Music', 'Exercising', 'Shopping', 'Dancing', 'Watching TV', 'Reading and Writing', 'Arts'])
    # ethnicity = random.choice(
    #     ['Black', 'White', 'Chinese', 'Indian', 'Hispanic'])
    # pref_ethnicity = random.choice(
    #     ['Black', 'White', 'Chinese', 'Indian', 'Hispanic'])
    # occupation = random.choice(
    #     ['Business', 'Science', 'Technology', 'Construction', 'Communication', 'Law'])
    # education = random.choice(
    #     ['Bachelors', 'Masters', 'PhD', 'Diploma', 'Associate Degree'])
    # personality = random.choice(['Introvert', 'Extrovert', 'Ambivert'])

    # sql = "INSERT INTO Regular (user_id, sex, age, height, leadership, ethnicity, personality, education, hobby, occupation, pref_sex, pref_ethnicity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # val = (2, sex, age,
    #        height, leadership, ethnicity, personality, education, hobby, occupation, pref_sex, pref_ethnicity)

    # mycursor.execute(sql, val)
    # mydb.commit()

    # to populate the set with users
    for i in range(2, records):
        # def populateScores(username):
        #     x = random.uniform(2, 9)
        #     sql = "INSERT INTO Scores (`userA username`, `userB username`, CSI, percentage, personality_score, leadership_score, hobby_score, gender_score, age_score, height_score, ethnicity_score, education_score, occupation_score, con_personality_score, con_leadership_score, con_hobby_score, con_gender_score, con_age_score, con_height_score, con_ethnicity_score, con_education_score, con_occupation_score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        #     val = ("Lanai", username, x, x*10, random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random(),
        #            random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random())

        #     mycursor.execute(sql, val)
        #     mydb.commit()

        # # creating users
        # first_name = fake.first_name()
        # last_name = fake.last_name()
        # username = first_name
        # email = last_name + username + "@gmail.com"
        # password = "1234"

        # sql = "INSERT INTO User (user_id, type, first_name, last_name, username, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        # val = (i, "Regular", first_name, last_name, username, email, password)

        # mycursor.execute(sql, val)
        # mydb.commit()

        # sex = random.choice(
        #     ['Female', 'Male'])

        # pref_sex = random.choice(
        #     ['Female', 'Male'])

        # height = random.randint(142, 198)
        # age = random.randint(22, 35)
        # leadership = random.choice(
        #     ['Autocratic', 'Laissez-Faire', 'Democratic'])
        # hobby = random.choice(
        #     ['Sports', 'Music', 'Exercising', 'Shopping', 'Dancing', 'Watching TV', 'Reading and Writing', 'Arts'])
        # ethnicity = random.choice(
        #     ['Black', 'White', 'Chinese', 'Indian', 'Hispanic'])
        # pref_ethnicity = random.choice(
        #     ['Black', 'White', 'Chinese', 'Indian', 'Hispanic'])
        # occupation = random.choice(
        #     ['Business', 'Science', 'Technology', 'Construction', 'Communication', 'Law'])
        # education = random.choice(
        #     ['Bachelors', 'Masters', 'PhD', 'Diploma', 'Associate Degree'])
        # personality = random.choice(['Introvert', 'Extrovert', 'Ambivert'])

        # sql = "INSERT INTO Regular (user_id, sex, age, height, leadership, ethnicity, personality, education, hobby, occupation, pref_sex, pref_ethnicity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # val = (mycursor.lastrowid, sex, age,
        #        height, leadership, ethnicity, personality, education, hobby, occupation, pref_sex, pref_ethnicity)

        # mycursor.execute(sql, val)
        # mydb.commit()

        # add them to set
            sql = "INSERT INTO joinSet (user_id, sid) VALUES (%s, %s)"
            val = (i, 4)

            mycursor.execute(sql, val)
            mydb.commit()
        # populateScores()


if __name__ == '__main__':
    populateSet(13)
    print("Sets Populated!")
