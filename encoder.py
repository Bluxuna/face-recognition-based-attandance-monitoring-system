import cv2
import face_recognition
import pickle
import os
import json
import mysql.connector
path = "IMAGE FOLDER PATH"
dct = {}
def writeInJson(data, filename):

    with open(filename, "a") as f:
        json.dump(data, f, indent=4)


def findEncoding(img):
    encodeList = []

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)[0]
    # print(encode)
    encodeList.append(encode.tolist())
    # data = {name: encode}
    # print(data)
    # for k in data:
    #     # print(k, data[k])
    #     x = data [k]
    #     # print(type(data[k]))
    #     data[k] = x.tolist()
    # # print(data)
    #
    # writeInJson( data, "data.json")
    return encodeList


def connect_to_database():
  try:
      connection = mysql.connector.connect(
          host="127.0.0.1",
          user="root",
          password="",
          database="ms")
      return connection
  except mysql.connector.Error as err:
      print("Error connecting to database:", err)
      return None
def get_data():
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            command = "SELECT * FROM student"
            cursor.execute(command)
            result = cursor.fetchall()

            for i in result:
                lst = []
                temp = path + f"//{i[4]}"
                answer = findEncoding(cv2.imread(temp))
                # print(i[0],answer)
                dct[i[0]] = [i[1], i[2], answer]
            connection.commit()
            print("data saved")
        except mysql.connector.Error as err:
            print("Error inserting data:", err)
        finally:
            connection.close()

# get_data()
# pathList = os.listdir('./photos')

# # Importing student images
# folderPath = 'photos'
# pathList = os.listdir(folderPath)
# names = []
# print(pathList)
# for i in pathList:
#     x = i[:len(i)-4]
#     names.append(x)
#
# imgList = []
# studentIds = []
# for path in pathList:
#     imgList.append(cv2.imread(os.path.join(folderPath, path)))
#     studentIds.append(os.path.splitext(path)[0])
#     fileName = f'{folderPath}/{path}'
# # print(studentIds)
# # print(imgList)
# cnt = 0
# for i in imgList:
#
#     findEncoding(i, names,cnt)
#     cnt += 1
