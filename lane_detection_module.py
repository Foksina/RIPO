# lane_detection_module.py

import cv2
import numpy as np

class LaneDetectionModule:
    def __init__(self, frame_width, frame_height):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.line_thickness = 2  # Grubość linii 
        self.warning_message = "Obiekt przed autem!"  # Komunikat ostrzegawczy
        self.trapez_points1 = []
        self.trapez_points2 = []
        self.trapez_points3 = []
    
    def detect_lane(self, frame):
        # Konwersja obrazu z formatu BGR do HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Definicja dolnej i górnej granicy kolorów dla drogi (ciemnoszary)
        lower_gray = np.array([0, 0, 100])
        upper_gray = np.array([30, 30, 150])

        # Utworzenie maski dla kolorów drogi
        mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)

        # Stosowanie maski na oryginalnym obrazie
        lane_segment = cv2.bitwise_and(frame, frame, mask=mask_gray)

        return lane_segment
    
    def draw_lane(self, frame, frame_count):       
        if frame_count % 7 == 0:
            # Detekcja linii za pomocą transformacji Hougha
            lane_segment = self.detect_lane(frame)

            # Konwersja obszaru drogi do skali szarości
            gray_lane = cv2.cvtColor(lane_segment, cv2.COLOR_BGR2GRAY)

            # Wykrywanie krawędzi w obszarze drogi
            edges = cv2.Canny(gray_lane, 50, 150)

            # Wyznaczenie konturów obszaru drogi
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Jeśli znaleziono kontury
            if contours:
                # Wybierz największy kontur (zakładając, że jest to obszar drogi)
                largest_contour = max(contours, key=cv2.contourArea)
            
                # Wyznacz współrzędne wierzchołków trapezu na podstawie konturu drogi
                trapez_points = self.get_trapez_points(largest_contour)

                bottom_left = trapez_points[0]
                top_left = trapez_points[1]
                top_right = trapez_points[2]
                bottom_right = trapez_points[3]

                # Obliczanie wysokości trapezu
                trapez_height = trapez_points[1][1] - trapez_points[0][1]
                helper = trapez_points[1][0] - trapez_points[0][0] # szerokosc miedzy dolnym a gornym wierzcholkiem
                helper2 = trapez_points[3][0] - trapez_points[2][0]
                # Trapez 1:
                self.trapez_points1 = np.array([bottom_left, [bottom_left[0]+(helper//3), bottom_left[1] + (trapez_height//3)], [bottom_right[0] - (helper2//3), bottom_right[1] + (trapez_height//3)], bottom_right], np.int32)
                # Trapez 2:
                self.trapez_points2 = np.array([[bottom_left[0]+(helper//3), bottom_left[1] + (trapez_height//3)], [top_left[0]-(helper//3), top_left[1] - (trapez_height//3)], [top_right[0] + (helper2//3), top_right[1] - (trapez_height//3)], [bottom_right[0] - (helper2//3), bottom_right[1] + (trapez_height//3)]], np.int32)
                # Trapez 3:
                self.trapez_points3 = np.array([ [top_left[0]-(helper//3), top_left[1] - (trapez_height//3)], top_left, top_right, [top_right[0] + (helper2//3), top_right[1] - (trapez_height//3)]], np.int32)

                cv2.polylines(frame, [self.trapez_points3], True, (0,255,0), self.line_thickness)
                cv2.polylines(frame, [self.trapez_points2], True, (0,255,255), self.line_thickness)
                cv2.polylines(frame, [self.trapez_points1], True, (0,0,255), self.line_thickness)

                #cv2.polylines(frame, [trapez_points], True, self.line_color, self.line_thickness)
        else:
            cv2.polylines(frame, [self.trapez_points3], True, (0,255,0), self.line_thickness)
            cv2.polylines(frame, [self.trapez_points2], True, (0,255,255), self.line_thickness)
            cv2.polylines(frame, [self.trapez_points1], True, (0,0,255), self.line_thickness)
        
        return frame
           
    def get_trapez_points(self, contour):
        # Wyznacz współrzędne wierzchołków trapezu na podstawie konturu drogi
        if contour is not None:
            # Oblicz współrzędne wierzchołków na podstawie wymiarów obrazu i konturu drogi
            bottom_left = (0, self.frame_height)
            bottom_right = (self.frame_width, self.frame_height)
            top_left = (contour[0][0][0] - 15, contour[0][0][1])
            top_right = (contour[-1][0][0] + 15, contour[-1][0][1])

            # Aktualizacja współrzędnych trapezu
            return np.array([bottom_left, top_left, top_right, bottom_right], np.int32)
        else:
            return np.array([[0, self.frame_height],
                             [int(self.frame_width * 0.4), int(self.frame_height * 0.6)],
                             [int(self.frame_width * 0.6), int(self.frame_height * 0.6)],
                             [self.frame_width, self.frame_height]], np.int32)
    
    def check_objects(self, objects, frame):
        if not objects:  # Jeśli lista obiektów jest pusta
            return

        # Słownik do przechowywania liczników dla każdej strefy
        counters = {'strefie 1': 0, 'strefie 2': 0, 'strefie 3': 0}

        for obj in objects:
            x, y, w, h, class_id = obj
            # Sprawdzanie, w którym trapezie znajduje się obiekt na podstawie współrzędnych
            for trapez_points, strefa in zip([self.trapez_points1, self.trapez_points2, self.trapez_points3], ['strefie 1', 'strefie 2', 'strefie 3']):
                if trapez_points is not None:
                    if cv2.pointPolygonTest(trapez_points, (x, y), False) >= 0 or \
                    cv2.pointPolygonTest(trapez_points, (x + w, y), False) >= 0 or \
                    cv2.pointPolygonTest(trapez_points, (x, y + h), False) >= 0 or \
                    cv2.pointPolygonTest(trapez_points, (x + w, y + h), False) >= 0:
                        print(f"Obiekt w {strefa}")
                        
                        # Inkrementacja licznika dla danej strefy
                        counters[strefa] += 1
                        # Sprawdzenie, czy licznik przekroczył 5
                        if counters['strefie 1'] >= 5:
                            cv2.putText(frame, f"Alert!", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
                            #print(f"Alert! Obiekt znajduje się w {strefa} przez przynajmniej 5 klatek!")
                        elif counters['strefie 2'] >= 5:
                            cv2.putText(frame, f"Alert!", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                        elif counters['strefie 3'] >= 5:
                            cv2.putText(frame, f"Alert!", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    else:
                        # Zerowanie licznika, jeśli obiekt nie jest w danej strefie
                        counters[strefa] = 0
        return frame