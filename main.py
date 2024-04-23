import tkinter as tk
from PIL import Image, ImageTk
import json
import networkx as nx
import matplotlib.pyplot as plt

class PointSelectorApp:
    def __init__(self, root, image_path):
        self.point_b_to_a_map = {}
        self.root = root
        self.image_path = image_path
        self.points_b = []  # Список для хранения точек B
        self.points_a = []  # Список для хранения точек A
        self.graph = nx.Graph()  # Инициализируем пустой граф
        self.current_point_type = 'B'  # По умолчанию считаем, что выбраны вершины (B)
        self.last_b_index = None  # Индекс последней точки B
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Point Selector")
        self.canvas_width = 1000
        self.canvas_height = 800
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        self.load_image()
        self.canvas.bind("<Button-1>", self.on_click)

        # Кнопки для переключения между точками B и A
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.b_button = tk.Button(self.button_frame, text="Select B Point", command=lambda: self.set_point_type('B'))
        self.b_button.pack(side=tk.LEFT)

        self.a_button = tk.Button(self.button_frame, text="Select A Point", command=lambda: self.set_point_type('A'))
        self.a_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.button_frame, text="Save Points", command=self.save_points)
        self.save_button.pack(side=tk.RIGHT)

        self.cabinet_label = tk.Label(self.button_frame, text="Enter Cabinet number:")
        self.cabinet_label.pack(side=tk.LEFT)
        self.cabinet_entry = tk.Entry(self.button_frame)
        self.cabinet_entry.pack(side=tk.LEFT)

    def load_image(self):
        image = Image.open(self.image_path)
        image = image.resize((self.canvas_width, self.canvas_height))
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=self.tk_image, anchor='nw')

    # Создание структуры данных для хранения связей между точками B и A
    point_b_to_a_map = {}

    def on_click(self, event):
        x, y = event.x, event.y
        if self.current_point_type == 'B':
            self.points_b.append((x, y))  # Добавляем точку B
            node_b = f"B_{len(self.points_b)}"
            self.graph.add_node(node_b)  # Добавляем вершину B в граф
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
            self.b_button.config(state=tk.DISABLED)
            self.a_button.config(state=tk.NORMAL)
            self.last_b_index = len(self.points_b)  # Обновляем индекс последней точки B

            # Инициализация point_b_to_a_map как словаря, если это еще не сделано
            if not hasattr(self, 'point_b_to_a_map'):
                self.point_b_to_a_map = {}

            # Добавление точки B в структуру данных
            self.point_b_to_a_map[(x, y)] = []
            print(f"Point B added at ({x}, {y})")

            # Если это не первая вершина B, соединяем ее с предыдущей
            if len(self.points_b) > 1:
                previous_node_b = f"B_{len(self.points_b) - 1}"
                self.graph.add_edge(previous_node_b, node_b)
        else:
            if self.points_b:  # Если уже выбрана точка B
                cabinet_number = self.cabinet_entry.get()  # Получаем номер кабинета из поля ввода
                if cabinet_number:
                    self.points_a.append(((x, y), cabinet_number))  # Добавляем точку A с указанным номером кабинета
                    node_a = f"A_{len(self.points_a)}"
                    self.graph.add_node(node_a)  # Добавляем вершину A в граф
                    self.graph.add_edge(f"B_{self.last_b_index}",
                                        node_a)  # Добавляем ребро от последней точки B к новой точке A
                    self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="blue")
                    print(f"Point A added at ({x}, {y}) with Cabinet number {cabinet_number}")

                    # Обновление структуры данных: добавление точки A к соответствующей точке B
                    self.point_b_to_a_map[self.points_b[-1]].append(((x, y), cabinet_number))
                else:
                    print("Please enter Cabinet number before selecting point A")

    def set_point_type(self, point_type):
        self.current_point_type = point_type
        if point_type == 'B':
            self.b_button.config(state=tk.DISABLED)
            self.a_button.config(state=tk.NORMAL)
        else:
            self.a_button.config(state=tk.DISABLED)
            self.b_button.config(state=tk.NORMAL)

    def save_points(self):
        data = {
            "point_b_to_a_map": {str(k): v for k, v in self.point_b_to_a_map.items()}
        }
        print(data)

        with open('floor_plan3.json', 'w') as f:
            json.dump(data, f, indent=4)
            print("Points saved to floor_plan.json")

        nx.draw(self.graph, with_labels=True)
        plt.show()

    def run(self):
        self.root.mainloop()



# Запуск приложения
root = tk.Tk()
root.geometry(f"{1200}x{1000}")  # Установка размеров окна
app = PointSelectorApp(root, 'D:\\PyCharmprojects\\pythonProject1\\3.jpg')
app.run()
