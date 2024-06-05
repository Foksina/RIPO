import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
from main import logic

class DetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacja Detekcji Obiektów")
        self.root.geometry("300x550")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.filename = "C:/Users/Kinga/Desktop/pwr/semestr 10/RiPO/Camera/examples/test5.mp4"
        self.detection_module = 0  # Default to YOLO
        self.car = 0
        self.bike = 0
        self.pedestrian = 0
        self.sound_alarms = 0
        self.visual_alarms = 0
        self.car_color = (255, 0, 0)
        self.bike_color = (182, 0, 178)
        self.pedestrian_color = (1, 98, 255)

        self.main_frame = ttk.Frame(root, padding=20)
        self.main_frame.pack(fill="both", expand=True)

        self.source_label = ttk.Label(self.main_frame, text="Wybierz źródło obrazu:")
        self.source_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.source_button = ttk.Button(self.main_frame, text="Wybierz plik", command=self.choose_file)
        self.source_button.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        self.model_label = ttk.Label(self.main_frame, text="Wybierz model:")
        self.model_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.model_var = tk.StringVar(value="YOLO")
        self.model_yolo_radio = ttk.Radiobutton(self.main_frame, text="YOLO", variable=self.model_var, value="YOLO", command=self.choose_YOLO)
        self.model_yolo_radio.grid(row=3, column=0, columnspan=2, sticky="w")
        self.model_yolo_light_radio = ttk.Radiobutton(self.main_frame, text="YOLO Lite", variable=self.model_var, value="YOLO Lite", command=self.choose_YOLO_Lite)
        self.model_yolo_light_radio.grid(row=4, column=0, columnspan=2, sticky="w")

        self.objects_label = ttk.Label(self.main_frame, text="Wybierz obiekty do detekcji:")
        self.objects_label.grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 5))
        self.car_var = tk.BooleanVar()
        self.car_checkbox = ttk.Checkbutton(self.main_frame, text="Samochody", variable=self.car_var, command=self.toggle_frame_colors)
        self.car_checkbox.grid(row=6, column=0, columnspan=2, sticky="w")
        self.bike_var = tk.BooleanVar()
        self.bike_checkbox = ttk.Checkbutton(self.main_frame, text="Rowery", variable=self.bike_var, command=self.toggle_frame_colors)
        self.bike_checkbox.grid(row=7, column=0, columnspan=2, sticky="w")
        self.pedestrian_var = tk.BooleanVar()
        self.pedestrian_checkbox = ttk.Checkbutton(self.main_frame, text="Piesi", variable=self.pedestrian_var, command=self.toggle_frame_colors)
        self.pedestrian_checkbox.grid(row=8, column=0, columnspan=2, sticky="w")

        self.alerts_label = ttk.Label(self.main_frame, text="Wybierz dodatkowe alerty:")
        self.alerts_label.grid(row=9, column=0, columnspan=2, sticky="w", pady=(10, 5))
        self.sound_var = tk.BooleanVar()
        self.sound_checkbox = ttk.Checkbutton(self.main_frame, text="Powiadomienia dźwiękowe", variable=self.sound_var, command=self.choose_sound_alarms)
        self.sound_checkbox.grid(row=10, column=0, columnspan=2, sticky="w")
        self.visual_var = tk.BooleanVar()
        self.visual_checkbox = ttk.Checkbutton(self.main_frame, text="Powiadomienia wizualne", variable=self.visual_var, command=self.choose_visual_alarms)
        self.visual_checkbox.grid(row=11, column=0, columnspan=2, sticky="w")

        self.car_frame_color_label = ttk.Label(self.main_frame, text="Kolor ramki dla samochodów:")
        self.car_frame_color_label.grid(row=13, column=0, sticky="w", pady=(10, 5))
        self.car_frame_color_button = ttk.Button(self.main_frame, text="Wybierz kolor", command=self.choose_car_frame_color, state=tk.DISABLED)
        self.car_frame_color_button.grid(row=13, column=1, pady=(10, 5), sticky="w")

        self.bike_frame_color_label = ttk.Label(self.main_frame, text="Kolor ramki dla rowerów:")
        self.bike_frame_color_label.grid(row=14, column=0, sticky="w", pady=(0, 5))
        self.bike_frame_color_button = ttk.Button(self.main_frame, text="Wybierz kolor", command=self.choose_bike_frame_color, state=tk.DISABLED)
        self.bike_frame_color_button.grid(row=14, column=1, pady=(0, 5), sticky="w")

        self.pedestrian_frame_color_label = ttk.Label(self.main_frame, text="Kolor ramki dla pieszych:")
        self.pedestrian_frame_color_label.grid(row=15, column=0, sticky="w", pady=(0, 10))
        self.pedestrian_frame_color_button = ttk.Button(self.main_frame, text="Wybierz kolor", command=self.choose_pedestrian_frame_color, state=tk.DISABLED)
        self.pedestrian_frame_color_button.grid(row=15, column=1, pady=(0, 10), sticky="w")

        self.start_button = ttk.Button(self.main_frame, text="Uruchom Detekcję", command=self.start_detection)
        self.start_button.grid(row=16, column=0, columnspan=2, pady=(10, 0), sticky="ew")

    def choose_file(self):
        self.filename = filedialog.askopenfilename()
        print("Wybrano plik:", self.filename)

    def choose_YOLO(self):
        self.detection_module = 0
        print("Wybrano model: YOLO")

    def choose_YOLO_Lite(self):
        self.detection_module = 1
        print("Wybrano model: YOLO Lite")

    def toggle_frame_colors(self):
        if self.car_var.get():
            self.car_frame_color_button.config(state=tk.NORMAL)
            self.car = 1
        else:
            self.car_frame_color_button.config(state=tk.DISABLED)
            self.car = 0

        if self.bike_var.get():
            self.bike_frame_color_button.config(state=tk.NORMAL)
            self.bike = 1
        else:
            self.bike_frame_color_button.config(state=tk.DISABLED)
            self.bike = 0
            
        if self.pedestrian_var.get():
            self.pedestrian_frame_color_button.config(state=tk.NORMAL)
            self.pedestrian = 1
        else:
            self.pedestrian_frame_color_button.config(state=tk.DISABLED)
            self.pedestrian = 0
    
    def choose_sound_alarms(self):
        self.sound_alarms = 1
    
    def choose_visual_alarms(self):
        self.visual_alarms = 1

    def choose_car_frame_color(self):
        color = colorchooser.askcolor()
        if color[0] is not None:  # Check if a color was selected
            # Reassign the entire tuple
            self.car_color = (int(color[0][2]), int(color[0][1]), int(color[0][0]))
            print("Wybrano kolor ramki dla samochodów:", self.car_color) 

    def choose_bike_frame_color(self):
        color = colorchooser.askcolor()
        if color[0] is not None:  # Check if a color was selected
            # Reassign the entire tuple
            self.bike_color = (int(color[0][2]), int(color[0][1]), int(color[0][0]))
            print("Wybrano kolor ramki dla rowerów:", self.bike_color)

    def choose_pedestrian_frame_color(self):
        color = colorchooser.askcolor()
        if color[0] is not None:  # Check if a color was selected
            # Reassign the entire tuple
            self.pedestrian_color = (int(color[0][2]), int(color[0][1]), int(color[0][0]))
            print("Wybrano kolor ramki dla pieszych:", self.pedestrian_color)
    
    def start_detection(self):
        logic(self.filename, self.detection_module, self.car, self.bike, self.pedestrian, self.car_color, self.bike_color, self.pedestrian_color, self.sound_alarms, self.visual_alarms)

if __name__ == "__main__":
    root = tk.Tk()
    app = DetectionApp(root)
    root.mainloop()
