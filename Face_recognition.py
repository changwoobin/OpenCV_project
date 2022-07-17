import cv2
import numpy as np
import os, glob

base_dir = './faces/'
def taPic():
    target_cnt = 400        
    cnt = 0                

    face_classifier = cv2.CascadeClassifier(\
                        './haarcascade_frontalface_default.xml')

    if not os.path.exists(dir_first):
        os.mkdir(dir_first)

    if not os.path.exists(dir):
        os.mkdir(dir)

    cap = cv2.VideoCapture(0+ cv2.CAP_DSHOW)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            img = frame.copy()
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)
            if len(faces) == 1:
                (x,y,w,h) = faces[0]
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 1)
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (200, 200))
                file_name_path = os.path.join(dir,  str(cnt) + '.jpg')
                cv2.imwrite(file_name_path, face)
                cv2.putText(frame, str(cnt), (x, y), cv2.FONT_HERSHEY_COMPLEX, \
                                1, (0,255,0), 2)
                cnt+=1
            else:
                if len(faces) == 0 :
                    msg = "no face."
                elif len(faces) > 1:
                    msg = "too many face."
                cv2.putText(frame, msg, (10, 50), cv2.FONT_HERSHEY_DUPLEX, \
                                1, (0,0,255))
            cv2.imshow('face record', frame)
            if cv2.waitKey(1) == 27 or cnt == target_cnt: 
                break
    cap.release()
    cv2.destroyAllWindows()      
    print("Collecting Samples Completed.")

def trainModel():
    train_data, train_labels = [], []


    dirs = [d for d in glob.glob(base_dir+"/*") if os.path.isdir(d)]
    print('Collecting train data set:')
    for dir in dirs:
        id = dir.split('_')[1]          
        files = glob.glob(dir+'/*.jpg')
        print('\t path:%s, %dfiles'%(dir, len(files)))
        for file in files:
            img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
            train_data.append(np.asarray(img, dtype=np.uint8))
            train_labels.append(int(id))

    train_data = np.asarray(train_data)
    train_labels = np.int32(train_labels)

    print('Starting LBP Model training...')
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(train_data, train_labels)
    model.write('./faces/all_face.xml')
    print("Model trained successfully!")

def start_Face_Recognition():
    min_accuracy = 85

    face_classifier = cv2.CascadeClassifier(\
                    './haarcascade_frontalface_default.xml')
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read(os.path.join(base_dir, 'all_face.xml'))

    dirs = [d for d in glob.glob(base_dir+"/*") if os.path.isdir(d)]
    names = dict([])
    for dir in dirs:
        dir = os.path.basename(dir)
        name, id = dir.split('_')
        names[int(id)] = name

    a = 0
    cap = cv2.VideoCapture(0+ cv2.CAP_DSHOW)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("no frame")
            break
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            face = frame[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            label, confidence = model.predict(face)
            if confidence < 400:
                accuracy = int( 100 * (1 -confidence/400))
                if accuracy >= min_accuracy:
                    print(names[label], accuracy)
                    a = 1
        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) == 27: #esc 
            print("인증 실패 했습니다.")
            break
        elif a == 1:
            print("인증 완료 되었습니다.")
            break
    cap.release()
    cv2.destroyAllWindows()    

dir_first = os.path.join('./faces/')
while 1:
    if not os.path.exists(dir_first):
        taPic()
        trainModel()

    n = int(input('무엇을 수행 할 까요?'))

    if n == 1:
        taPic()
        trainModel()
    elif n == 2:
        start_Face_Recognition()
        break
    elif n == 3:
        print("시스템을 종료합니다.")