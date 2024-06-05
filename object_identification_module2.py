import cv2
import numpy as np

class ObjectIdentificationModuleLite:
    def __init__(self, car_var = 0, bike_var = 0, pedestrian_var = 0, car_color = (255, 0, 0), bike_color = (182, 0, 178) , pedestrian_color = (1, 98, 255)):
        # YOLO - Lite
        self.net = cv2.dnn.readNet('yolov3-tiny.weights', 'yolov3-tiny.cfg')
        self.classes = []
        with open('coco.names', 'r') as f: # Wczytanie nazw klas
            self.classes = f.read().splitlines()
        
        self.detected_objects = [] 

        self.car_var = car_var
        self.bike_var = bike_var
        self.pedestrian_var = pedestrian_var
        self.car_color = car_color
        self.bike_color = bike_color 
        self.pedestrian_color = pedestrian_color

    def identify_objects(self, frame):
        # Identyfikacja obiektów - wykrywanie samochodów, pieszych i rowerzystów za pomocą modelu YOLOv3 - You Only Look Once
        height, width, _ = frame.shape

        # Przygotowanie wejścia do sieci neuronowej
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)  
                                                    # frame - obraz wejściowy 
                                                    # 1 / 255.0 - współczynnik skalowania pikseli w zakresie od 0 do 1
                                                    # (416, 416) - rozmiar, do którego obraz zostanie przeskalowany przed przetworzeniem (wymagany przez YOLOv3)
                                                    # swapRB=True - zamiana kanałów kolorów z BGR na RGB
                                                    #crop=False - obraz nie jest przycinany do określonego rozmiaru
        self.net.setInput(blob) # ustawia blob jako wejście dla sieci neuronowej

        # Przejście przez sieć neuronową i uzyskanie wyjść
        output_layers_names = self.net.getUnconnectedOutLayersNames()
        layer_outputs = self.net.forward(output_layers_names) # przekazanie danych przez sieć, zwraca wyniki dla określonych warstw wyjściowych

        # Przetwarzanie wyjść i wykrywanie obiektów
        boxes = []
        confidences = []
        class_ids = []

        self.detected_objects = []

        for output in layer_outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id] # pewność powyżej 0.5 to uznajemy za wykryty obiekt
                if confidence > 0.5 and (class_id in [0,2,3]): # Indeks 0: "person", 2: "car", 3: "bicycle"
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                    self.detected_objects.append((x, y, w, h, class_id))

        # Wykorzystanie Non-Maximum Suppression w celu usunięcia duplikatów
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4) # 0.4 - procentowy próg nakładania się prostokątów, powyżej prostokąty uznawane są za nakładające się 

        # Rysowanie prostokątów wokół wykrytych obiektów
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = self.classes[class_ids[i]]
                if class_ids[i] == 3 and self.bike_var==1: #  dla rowerzystow
                    color = self.bike_color
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                elif class_ids[i] == 2 and self.car_var==1: #  dla samochodów
                    color = self.car_color
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                elif self.pedestrian_var == 1:
                    color = self.pedestrian_color #  dla pieszych
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
        return frame
    
    def get_detected_objects(self):
        return self.detected_objects
