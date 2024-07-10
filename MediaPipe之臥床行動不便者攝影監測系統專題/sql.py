import cv2
import mediapipe as mp
import math
import numpy as np
import datetime
import mysql.connector
import pygame

# 初始化 pygame
pygame.mixer.init()

# 建立 VideoWriter
fourcc = cv2.VideoWriter_fourcc(*"XVID")  # 指定編碼方式
output_file = cv2.VideoWriter("C:/xampp/htdocs/captured_images/fall.avi", fourcc, 20.0, (640, 480))
image_count = 0

# 建立 MySQL 連線
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
   
)

cursor = db.cursor()
# 刪除現有的 'mydb' 資料庫
cursor.execute("DROP DATABASE IF EXISTS`mydb`;")
# 創建新的 'mydb' 資料庫
cursor.execute("CREATE DATABASE `mydb`;")
# 選擇 'mydb' 資料庫
cursor.execute("USE `mydb`;")
# 指定要刪除的資料表名稱
table_name = "pose_data"
# 刪除現有的 'pose_data' 資料表
drop_table_query = f"DROP TABLE IF EXISTS `{table_name}`;"
cursor.execute(drop_table_query)
print(f"Table {table_name} dropped successfully.")  # 新增的除錯信息


# 執行創建表的SQL
create_table_query = "CREATE TABLE `pose_data` (datetime DATETIME, left_eye_x VARCHAR(255), left_eye_y VARCHAR(255),right_eye_x VARCHAR(255),right_eye_y VARCHAR(255));"
cursor.execute(create_table_query)
create_table_query_2 = "ALTER TABLE `pose_data` ADD COLUMN right_shoulder_x VARCHAR(255), ADD COLUMN right_shoulder_y VARCHAR(255), ADD COLUMN left_shoulder_x VARCHAR(255), ADD COLUMN left_shoulder_y VARCHAR(255), ADD COLUMN right_elbow_x VARCHAR(255);"
cursor.execute(create_table_query_2)
create_table_query_3 = "ALTER TABLE `pose_data` ADD COLUMN right_elbow_y VARCHAR(255), ADD COLUMN left_elbow_x VARCHAR(255), ADD COLUMN left_elbow_y VARCHAR(255), ADD COLUMN left_hip_x VARCHAR(255), ADD COLUMN left_hip_y VARCHAR(255),ADD COLUMN right_hip_x VARCHAR(255),ADD COLUMN right_hip_y VARCHAR(255);"
cursor.execute(create_table_query_3)
create_table_query_4 = "ALTER TABLE `pose_data` ADD COLUMN left_knee_x VARCHAR(255), ADD COLUMN left_knee_y VARCHAR(255), ADD COLUMN right_knee_x VARCHAR(255), ADD COLUMN right_knee_y VARCHAR(255), ADD COLUMN left_heel_x VARCHAR(255),ADD COLUMN left_heel_y VARCHAR(255),ADD COLUMN right_heel_x VARCHAR(255);"
cursor.execute(create_table_query_4)
create_table_query_5 = "ALTER TABLE `pose_data` ADD COLUMN right_heel_y VARCHAR(255), ADD COLUMN right_index_x VARCHAR(255), ADD COLUMN right_index_y VARCHAR(255), ADD COLUMN left_index_x VARCHAR(255), ADD COLUMN left_index_y VARCHAR(255),ADD COLUMN stage VARCHAR(255);"
cursor.execute(create_table_query_5)


# 計算三個點之間的角度
def calculate_angle(a, b, c):
    a = np.array(a)# 第一個點
    b = np.array(b)# 中間點
    c = np.array(c)# 結束點

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle#計算三個點所形成的夾角，並返回最終的角度值


# 創建 mediapipe 的 drawing_utils 和 pose 物件
mp_drawing = mp.solutions.drawing_utils# 物件用於繪製工具功能
mp_pose = mp.solutions.pose# 物件用於姿勢估計（例如，偵測人體關鍵點）
# 創建 mediapipe 的 face_detection 物件
mp_face_detection = mp.solutions.face_detection # 物件用於使用 mediapipe 進行人臉偵測
cap = cv2.VideoCapture(0)


counter = 0# 定義一個變數 counter，初始值為 0
stage = None# 定義一個變數 stage，初始值為 None


# 使用指定參數初始化姿勢估計和人臉偵測物件
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
    mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        ret, frame = cap.read() # 讀取攝像頭影像
        if ret:
            # 將影像轉換為 RGB 格式
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False#為了讓下一行更有效率

             # 進行姿勢估計和人臉偵測
            results = pose.process(image)# 進行姿勢估計
            faces = face_detection.process(image)# 進行人臉偵測
             
            # 取得關鍵點預測結果
            pose_landmarks = results.pose_landmarks

            if pose_landmarks is not None:
            # 將關鍵點預測結果轉換為陣列
                pose_array = np.array([[lm.x, lm.y, lm.z, lm.visibility] for lm in pose_landmarks.landmark]).flatten()
    

                # 印出格式化的關鍵點數據
                print("[" + " ".join(f"{val:12.5f}" for val in pose_array) + "]")
                print("Shape of pose array:", pose_array.reshape(1, -1).shape)
            else:
                print("No pose landmarks detected.")
             
             
             # 將影像轉回 BGR 格式
            image.flags.writeable = True#重啟圖片寫入標記功能
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 取得當前的時間和日期
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")

            # 提取關鍵點資訊（姿勢估計的結果）
            try:
                landmarks = results.pose_landmarks.landmark

                # 人體座標位置
                left_eye = [landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].y]#左眼 X 和 Y 座標值
                right_eye = [landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].y]#右眼 X 和 Y 座標
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]#左肩 X 和 Y 座標
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]#右肩 X 和 Y 座標
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]#左肘 X 和 Y 座標
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]#右肘 X 和 Y 座標
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]#左臀部 X 和 Y 座標
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]#右臀部 X 和 Y 座標
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]#左膝跟 X 和 Y 座標
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]#右膝跟 X 和 Y 座標  
                left_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]#左腳跟 X 和 Y 座標
                right_heel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]#右腳跟 X 和 Y 座標
                right_index = [landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y]#右手食指 X 和 Y 座標
                left_index = [landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y]#左手食指 X 和 Y 座標

                right_heel_x, right_heel_y = landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y 
                right_hip_x, right_hip_y = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y 
                right_shoulder_x, right_shoulder_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
                

                                            # 計算全身長
                                            # 計算眼和腳跟的 x 和 y 座標
                left_eye_x, left_eye_y = landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].y
                left_heel_x, left_heel_y = landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y
                                             # 計算左眼到左腳跟的勾股距離，以獲得全身長
                all_body_len = math.sqrt((left_eye_y - left_heel_y)**2 + (left_eye_x - left_heel_x)**2)


                             # 計算軀幹長度
                             # 計算肩和臀部的 x 和 y 座標
                left_shoulder_x, left_shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
                left_hip_x, left_hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
                           # 計算肩到臀部勾股距離，以獲得軀幹長度
                torso_len = math.sqrt((left_shoulder_y - left_hip_y)**2 + (left_shoulder_x - left_hip_x)**2)


                # 計算大小腿長
                # 計算腳跟和膝蓋的 x 和 y 座標
                left_heel_x, left_heel_y = landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y
                left_knee_x, left_knee_y = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y
                # 計算腳跟到膝蓋的勾股距離，以獲得大小腿長度
                leg_len = math.sqrt((left_heel_y - left_knee_y)**2 + (left_heel_x - left_knee_x)**2)


                # 設定軀幹長和大小腿長的比例閾值，用於判斷是否嘗試起身
                torso_leg_ratio_threshold = 0.8
                #print("Angle Threshold:", angle_threshold)

                # 設定角度閾值，用於判斷是否平躺
                angle_threshold = 20  # 可根據需要調整       
                #print("Angle Threshold:", angle_threshold)   
                

                # 設定軀幹與全身長的比例閾值，用於判斷是否跌倒
                torso_body_ratio_threshold = 0.6
                #print("軀幹與全身長的比例閾值:", torso_body_ratio_threshold)     


                # 判斷是否嘗試起身
                if ((right_eye[0] > 0.5) and (right_shoulder[0] > 0.5)) or ((left_eye[0] > 0.5) and (left_shoulder[0] < 0.5)):
                    # 計算軀幹長和大小腿長的比例
                    torso_leg_ratio = torso_len / leg_len
                    #print("torso_leg_ratio:", torso_leg_ratio)
                    
 
                angle1 = calculate_angle(left_eye, left_hip, left_heel)# 計算左側的角度
                angle2 = calculate_angle(right_eye, right_hip, right_heel)# 計算右側的角度

                # 將角度數值顯示在影像上
                cv2.putText(image, str(angle1),
                            tuple(np.multiply(left_hip, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                )
                cv2.putText(image, str(angle2),
                            tuple(np.multiply(right_hip, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                )


                #print(f"left_eye={left_eye}")
                #print(f"right_eye={right_eye}")

                #print(f"right_shoulder={right_shoulder}")
                #print(f"left_shoulder={left_shoulder}")

                #print(f"right_elbow={right_elbow}")
                #print(f"left_elbow={left_elbow}")

                #print(f"left_hip={left_hip}")
                #print(f"right_hip={right_hip}")

                #print(f"left_knee={left_knee}")
                #print(f"right_knee={right_knee}")

                #print(f"left_heel={left_heel}")
                #print(f"right_heel={right_heel}")

                #print(f"right index={right_index}")
                #print(f"left index={left_index}")


                 # 如果角度接近 180 或 150，而且另一個角度也接近 180 或 150，則視為安全狀態
                if (abs(angle1 - 180) < angle_threshold or abs(angle1 - 150) < angle_threshold) and \
                   (abs(angle2 - 180) < angle_threshold or abs(angle2 - 150) < angle_threshold):
                           stage = "safe :)"
                else:
                      # 如果軀幹和大小腿的比例大於閾值，則視為試圖起身的狀態
                      if torso_leg_ratio > torso_leg_ratio_threshold:
                         stage = "stand up !!"
                      else:
                            # 如果軀幹和全身長的比例小於閾值，則視為跌倒的狀態
                           if (torso_len / all_body_len) < torso_body_ratio_threshold:
                                   stage = "fallen :("
                           else:
                                  stage = None
            except:
                  pass

            # 在影像上繪製一個矩形
            cv2.rectangle(image, (0,0), (350,160), (245,117,16), -1)

           # 顯示「Rep data」（重複資料）的文字
            cv2.putText(image, 'Condition: ', (15,12),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str("Calculating Angles"),
            (100,12),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

            # 顯示「Stage data」（階段資料）的文字
            cv2.putText(image, 'STAGE: ', (10,50),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage,
            (10,100),
            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)

              # 在影像上繪製時間和日期
            cv2.putText(image, f"Time: {current_time}", (30,150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(image, f"Date: {current_date}", (30,130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

             # 應用臉部模糊
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                 face_roi = image[y:y + h, x:x + w]
                 blurred_face = cv2.GaussianBlur(face_roi, (99, 99), 30)
                 image[y:y + h, x:x + w] = blurred_face

            cv2.imshow('Mediapipe Feed', image)
            output_file.write(image)
            # 保存圖像
            cv2.imwrite(f"fall_image_{image_count}.jpg", image)
            image_count += 1
             # 保存視頻帧
            output_file.write(image)

            # 將判斷結果寫入資料庫
            try:
                 sql = "INSERT INTO pose_data (datetime, left_eye_x, left_eye_y, right_eye_x, right_eye_y, " \
                       "right_shoulder_x, right_shoulder_y, left_shoulder_x, left_shoulder_y, right_elbow_x, " \
                       "right_elbow_y, left_elbow_x, left_elbow_y, left_hip_x, left_hip_y, right_hip_x, right_hip_y, " \
                       "left_knee_x, left_knee_y, right_knee_x, right_knee_y, left_heel_x, left_heel_y, right_heel_x, " \
                       "right_heel_y, right_index_x, right_index_y, left_index_x, left_index_y, stage) " \
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                 val = (current_date + " " + current_time, left_eye[0], left_eye[1], right_eye[0], right_eye[1],
                       right_shoulder[0], right_shoulder[1], left_shoulder[0], left_shoulder[1],
                       right_elbow[0], right_elbow[1], left_elbow[0], left_elbow[1],
                       left_hip[0], left_hip[1], right_hip[0], right_hip[1],
                       left_knee[0], left_knee[1], right_knee[0], right_knee[1],
                       left_heel[0], left_heel[1], right_heel[0], right_heel[1],
                       right_index[0], right_index[1], left_index[0], left_index[1], stage)
                 cursor.execute(sql, val)
                 db.commit()
            except Exception as e:
                print("Error inserting data into MySQL database:", e)
                
             # 在特定的情況下播放音效
            if stage == "fallen :(":
                 pygame.mixer.music.load("fall.mp3")
                 pygame.mixer.music.play()  

            if cv2.waitKey(10) == ord('q'):
                break

        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

cap.release()
cv2.destroyAllWindows()
          

