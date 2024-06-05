import cv2
from image_processing_module import ImageProcessingModule
from object_identification_module2 import ObjectIdentificationModuleLite
from object_identification_module import ObjectIdentificationModule
from lane_detection_module import LaneDetectionModule

#rozdzielczość
new_width = 320
new_height = 240

def logic(filename, detection_module, car_var, bike_var, pedestrian_var, car_color, bike_color, pedestrian_color, sound_alarms, visual_alarms):
    # Inicjalizacja kamery (tutaj symulowana za pomocą wideo)
    cap = cv2.VideoCapture(filename)

    image_processor = ImageProcessingModule()
    lane_detector = LaneDetectionModule(new_width, new_height)

    # wybór detekcji
    if detection_module == 1:
        object_identifier = ObjectIdentificationModuleLite(car_var, bike_var, pedestrian_var, car_color, bike_color, pedestrian_color)
    else:
        object_identifier = ObjectIdentificationModule(car_var, bike_var, pedestrian_var, car_color, bike_color, pedestrian_color)


    frame_count = 0  

    while(cap.isOpened()):
        ret, frame = cap.read() 

        if ret:
            
            processed_frame = image_processor.process_image(frame, new_width, new_height) 
            identified_frame = object_identifier.identify_objects(processed_frame) 

            lane_frame = lane_detector.draw_lane(processed_frame, frame_count)

            objects = object_identifier.get_detected_objects()
            lane_frame = lane_detector.check_objects(objects, lane_frame, frame_count, sound_alarms, visual_alarms)

            frame_count = frame_count +1

            cv2.imshow('Detected Objects with Lane', lane_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    logic()