import os
import cv2
from image_processing_module import ImageProcessingModule
from object_identification_module import ObjectIdentificationModule
from lane_detection_module import LaneDetectionModule

#rozdzielczość
new_width = 320
new_height = 240

def main():
    examples_folder = 'examples'
    test_video_path = os.path.join(examples_folder, 'test4.mp4')

    # Inicjalizacja kamery (tutaj symulowana za pomocą wideo)
    cap = cv2.VideoCapture(test_video_path) 

    image_processor = ImageProcessingModule()
    object_identifier = ObjectIdentificationModule()
    lane_detector = LaneDetectionModule(new_width, new_height)


    frame_count = 0  

    while(cap.isOpened()):
        ret, frame = cap.read() 

        if ret:
            
            processed_frame = image_processor.process_image(frame, new_width, new_height) 
            identified_frame = object_identifier.identify_objects(processed_frame) 

            lane_frame = lane_detector.draw_lane(processed_frame, frame_count)
            frame_count = frame_count +1

            objects = object_identifier.get_detected_objects()
            lane_frame = lane_detector.check_objects(objects, lane_frame)

            cv2.imshow('Detected Objects with Lane', lane_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()