# -*- coding: UTF-8 -*-
#http://qiita.com/Algebra_nobu/items/a488fdf8c41277432ff3
import cv2
import os


#人の認識
f_cascade = cv2.CascadeClassifier('⁨haarcascade_fullbody.xml')

DEVICE_ID = 0
cap = cv2.VideoCapture(DEVICE_ID)
ret, frame = cap.read()
# カメラの起動
while(ret):
    #物体認識（人）の実行
    facerect = f_cascade.detectMultiScale(frame)

    #検出した人を囲む矩形の作成
    for rect in facerect:
        cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), (255, 255, 255), thickness=2)

        # text = 'p'
        # font = cv2.FONT_HERSHEY_PLAIN
        # cv2.putText(frame,text,(rect[0],rect[1]-10),font, 2, (255, 255, 255), 2, cv2.LINE_AA)

    # 表示
    window_name = 'window'
    # ウィンドウに表示
    cv2.imshow(window_name, frame)

    # ESCキー押下で終了
    if cv2.waitKey(30) & 0xff == 27:
        break

    end_flag, frame = cap.read()

cap.release()
cv2.destroyAllWindows()
