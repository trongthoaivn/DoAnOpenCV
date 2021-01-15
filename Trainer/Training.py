import csv
import os
import cv2
import face_recognition

CURR_DIR = os.path.dirname(__file__)
images = []
known_face_encodings = []
known_face_names = []
attendance_list = os.listdir('%s/Dataset'%CURR_DIR[0:13])
path = '%s/Dataset'%CURR_DIR[0:13]
for r in attendance_list:
    img_non = cv2.imread("%s/%s" % (path, r))
    images.append(img_non)
    known_face_names.append("%s" % os.path.splitext(r)[0])
for it in images:
    it = cv2.cvtColor(it, cv2.COLOR_BGR2RGB)
    face = face_recognition.face_locations(it)
    img_encode = face_recognition.face_encodings(it, face)[0]
    known_face_encodings.append(img_encode)
with open('%s/data.csv' % CURR_DIR, 'w', newline='') as file:
    writer = csv.writer(file)
    for name in known_face_names:
        for face in known_face_encodings:
            value = face
            writer.writerow([name, face])
            known_face_encodings.remove(value)
            break

print(CURR_DIR[0:13])
print('complete')
