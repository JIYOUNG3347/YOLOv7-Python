import cv2
import numpy as np

# 웹캠 신호 받기
VideoSignal = cv2.VideoCapture(0)
# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet("yolov2-tiny.weights","yolov2-tiny.cfg")

# YOLO NETWORK 재구성
classes = []
with open("yolo.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]

while True:
    # 웹캠 프레임
    ret, frame = VideoSignal.read()
    print(frame)
    h, w, c = frame.shape

    # YOLO 입력
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
    True, crop=False)
    YOLO_net.setInput(blob)
    outs = YOLO_net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:

        for detection in out:

            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                dw = int(detection[2] * w)
                dh = int(detection[3] * h)
                # Rectangle coordinate
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                boxes.append([x, y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)


    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            score = confidences[i]

            # 경계상자와 클래스 정보 이미지에 입력
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
            cv2.putText(frame, label, (x, y - 20), cv2.FONT_ITALIC, 0.5,
            (255, 255, 255), 1)

    cv2.imshow("YOLOv3", frame)

    if cv2.waitKey(100) > 0:
        break
