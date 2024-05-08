# lane_detection_module.py

import cv2
import numpy as np

class LaneDetectionModule:
    def __init__(self, frame_width, frame_height):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.line_thickness = 2  # Grubość linii
        self.line_color = (0, 255, 0)  # Kolor linii (zielony)
        self.warning_message = "Obiekt przed autem!"  # Komunikat ostrzegawczy
    
    def detect_lines(self, frame):
        # Filtracja kolorów
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        print("HSV:", hsv)
        lower_gray = np.array([0, 0, 20]) 
        upper_gray = np.array([180, 100, 80])
        mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)
        print("mask", mask_gray)

        # Progowanie
        _, thresh = cv2.threshold(mask_gray, 150, 255, cv2.THRESH_BINARY)

        # Erozja i dylatacja
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        # Transformacja probabilistyczna Hougha
        lines = cv2.HoughLinesP(opening, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=50)
        print("Detected lines:", lines)
        return lines
    
    def draw_lane(self, frame):       
        # Detekcja linii za pomocą transformacji Hougha
        lines = self.detect_lines(frame)

        # Wyznaczenie współrzędnych trapezu na podstawie wykrytych linii
        trapez_points = self.get_trapez_points(lines)

        # Rysowanie trapezu jako obszaru przed autem
        cv2.polylines(frame, [trapez_points], True, self.line_color, self.line_thickness)

        return frame
    
    def get_trapez_points(self, lines):
        if lines is None:
            return np.array([[0, self.frame_height],
                             [int(self.frame_width * 0.4), int(self.frame_height * 0.6)],
                             [int(self.frame_width * 0.6), int(self.frame_height * 0.6)],
                             [self.frame_width, self.frame_height]], np.int32)

        # Zebranie punktów granicznych linii lewej i prawej
        left_points = []
        right_points = []

        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x2 - x1 != 0:  # Unikanie dzielenia przez zero
                slope = (y2 - y1) / (x2 - x1)
                if abs(slope) > 0.5:  # Odrzucenie linii o zbyt stromym nachyleniu
                    continue
                if slope < 0:
                    left_points.append((x1, y1))
                    left_points.append((x2, y2))
                else:
                    right_points.append((x1, y1))
                    right_points.append((x2, y2))

        # Sortowanie punktów
        left_points = sorted(left_points, key=lambda x: x[0])
        right_points = sorted(right_points, key=lambda x: x[0])

        if left_points and right_points:
            # Dolne punkty trapezu
            bottom_left = (0, self.frame_height)
            bottom_right = (self.frame_width, self.frame_height)

            # Wysokość trapezu
            trap_height = int(self.frame_height * 0.2)

            # Górne punkty trapezu
            upper_left_x = left_points[0][0]
            upper_right_x = right_points[-1][0]
            upper_left = (upper_left_x, int(self.frame_height * 0.6) - trap_height)
            upper_right = (upper_right_x, int(self.frame_height * 0.6) - trap_height)

            # Aktualizacja współrzędnych trapezu
            return np.array([bottom_left, upper_left, upper_right, bottom_right], np.int32)
        else:
            return np.array([[0, self.frame_height],
                             [int(self.frame_width * 0.4), int(self.frame_height * 0.6)],
                             [int(self.frame_width * 0.6), int(self.frame_height * 0.6)],
                             [self.frame_width, self.frame_height]], np.int32)
    
    def check_objects(self, objects):
        if not objects:  # Jeśli lista obiektów jest pusta
            return
        
        # Sprawdzanie, czy obiekty znajdują się przed autem (przez linie)

        for obj in objects:
            x, y, w, h, class_id = obj
            if y + h > self.frame_height * 0.6:  # Obiekt w strefie 1
                print("Obiekt w strefie 1")
            elif y + h > self.frame_height * 0.8:  # Obiekt w strefie 2
                print("Obiekt w strefie 2")
            elif y + h > self.frame_height * 0.9:  # Obiekt w strefie 3
                print("Obiekt w strefie 3")