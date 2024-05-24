import json
import cv2
import face_recognition
import numpy as np
import mysql.connector
import threading
from concurrent.futures import ThreadPoolExecutor
import datetime
import encoder

encoder.get_data()
dct = encoder.dct
reverse_dct = {}
for k in dct:
    reverse_dct[dct[k][0] + ' ' + dct[k][1]] = k
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

def insert(id):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            commandz = f"SELECT schedule.ScheduleID FROM class INNER JOIN student on student.ClassID=class.ClassID inner JOIN schedule on class.ClassID=schedule.ClassID WHERE HOUR(schedule.Date)=hour(CURRENT_TIME) and student.StudentID={id};"
            cursor.execute(commandz)
            r = cursor.fetchone()
            print(r)
            if r == None:
                text_box[:] = red
            else:
                #command = f"INSERT INTO attandance (PersonID, ScheduleID, Who) VALUES (%s, %s, %s)"
                command = "INSERT INTO attandance (PersonID, ScheduleID, Who) VALUES ('"+str(id)+"','"+str(r[0])+"','0')"
                #values = (id, r, "0")
                cursor.execute(command)
                print(r)

                print("data saved11")
            connection.commit()
        except mysql.connector.Error as err:
            print("Error inserting data:", err)
        finally:
            connection.close()



def compare_face(encoding, known_encodings):
  matches = face_recognition.compare_faces(known_encodings, encoding)
  faceDis = face_recognition.face_distance(known_encodings, encoding)
  # ... (your logic to handle matches and distances)
  return matches, faceDis
def face_locations_wrapper(imgS):
  return face_recognition.face_locations(imgS)

def face_encodings_wrapper(imgS, faceCurFrame):
  return face_recognition.face_encodings(imgS, faceCurFrame)

cap = cv2.VideoCapture(0)
# cap.set(3,840)
# cap.set(4,480)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
names = []
encodings = []

red, green, white = (0, 0, 255), (0, 255, 0), (255, 255, 255)

background = np.zeros(
    (800, 800, 3),
    dtype=np.uint8
)

background[:] = red

text_box = np.zeros(
    (100, 700, 3),
    dtype=np.uint8
)
text_box[:] = white

# with open('data.json', 'r') as f:
#     data = json.load(f)
    # print(data)
for k in dct:
    var = dct[k][0] + " " + dct[k][1]
    names.append(var)
    encodings.append(dct[k][2][0])
    # print(names)
modeType, counter, id = 0, 0, -1
cnt =0
# print(encodings)
while True:


    succes, img = cap.read()
    txt = "uknown"
    clr = (0,0,255)
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    # faceCurFrame = face_recognition.face_locations(imgS)
    # encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    # print("this-> ",faceCurFrame)
    with ThreadPoolExecutor() as executor:
        # Submit tasks for concurrent execution
        future_locations = executor.submit(face_locations_wrapper, imgS)
        future_encodings = executor.submit(face_encodings_wrapper, imgS, future_locations.result())

        # Retrieve results from the futures
        faceCurFrame = future_locations.result()
        encodeCurFrame = future_encodings.result()


    if faceCurFrame:

        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodings, encodeFace)
            faceDis = face_recognition.face_distance(encodings, encodeFace)
            # print("matches", matches)
            #
            # print("faceDis", faceDis)
            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                top, right, bottom, left = faceLoc
                top, right, bottom, left = faceLoc
                top, right, bottom, left = top*4, right*4, bottom*4, left*4
                cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img,
                            names[matchIndex].replace("_", " "),
                            (left, bottom),
                            font, 1,
                            (0, 255, 255),
                            1,
                            cv2.LINE_4)
                txt = names[matchIndex].replace("_", " ")

                cnt += 1
                x = datetime.datetime.now()

                if cnt == 12:
                    id = reverse_dct[txt]
                    insert(id)
                    cnt =0




                clr = (0, 255, 0)
                background[:] = green
            else:
                top, right, bottom, left = faceLoc
                top, right, bottom, left = faceLoc
                top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img,
                            "uknown",
                            (left, bottom),
                            font, 1,
                            (0, 0, 255),
                            2,
                            cv2.LINE_4)

                # background[650:650 + 100, 60:60 + 500] = names[matchIndex]

    else:
        background[:] = red
        txt = "not detected"
        clr = (0, 0, 255)
    background[162:162 + 480, 55:55 + 640] = img
    background[650:650 + 100, 60:60 + 700] = text_box
    background = cv2.putText(
        img=background,
        text=txt,
        org=(60, 690),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=1.5,
        color=clr,
        thickness=2
    )
    # background[650:650 + 100, 60:60 + 500] = "uknown"

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # cv2.imshow("add user", img)

    cv2.imshow("system", background)
    # cv2.imshow("test_box", text_box)
    cv2.waitKey(1)