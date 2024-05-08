import cv2

class ImageProcessingModule:
    def __init__(self):
        pass

    def process_image(self, frame, new_width = 320, new_height=240):
        # Zmniejszenie rozdzielczości obrazu
        resized_frame = cv2.resize(frame, (new_width, new_height))

        return resized_frame
