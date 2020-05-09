import mysql.connector
import random

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="csi"
)

mycursor = mydb.cursor()


def populateScores(records):
    for p in range(2, 16):
        for i in range(p+1, records+1):
            val = float("{:.2f}".format(random.uniform(0, 1)))

            sql = "INSERT INTO Scores (user_id, match_id, score) VALUES (%s, %s, %s)"
            val = (p, i, val)

            mycursor.execute(sql, val)
            mydb.commit()

            # print(p, i, val)


if __name__ == '__main__':
    populateScores(12)
    print("Scores Recorded!")
