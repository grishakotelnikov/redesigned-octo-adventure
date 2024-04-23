from tkinter import simpledialog, messagebox

from PIL import Image, ImageTk
import json
import networkx as nx
import tkinter as tk

from matplotlib import pyplot as plt


def load_data_from_json(file_path):
    """Загрузка данных из JSON-файла."""
    with open(file_path, 'r') as f:
        return json.load(f)

def create_graph(data):
    """Создание графа из данных."""
    G = nx.Graph()
    prev_key = None
    first_key = None
    for key, value in data['point_b_to_a_map'].items():
        G.add_node(key)
        if first_key is None:
            first_key = key
        if prev_key is not None:
            G.add_edge(prev_key, key)
        prev_key = key
        if isinstance(value, list):
            for item in value:
                for k, v in item.items():
                    if k == "value":
                        v = str(v)
                        G.add_edge(key, v)
        elif isinstance(value, dict):
            for k, v in value.items():
                if k == "value":
                    v = str(v)
                    G.add_edge(key, v)
    if first_key is not None and prev_key is not None:
        G.add_edge(prev_key, first_key)
    return G

def find_vertex_by_room(data, room_number):
    """Находит вершины по номеру комнаты."""
    vertices = []
    for vertex, room_data in data['point_b_to_a_map'].items():
        if isinstance(room_data, list):
            for item in room_data:
                if isinstance(item, dict) and item.get('value') == room_number:
                    vertices.append(vertex)
                elif isinstance(item, list) and item[1] == room_number:
                    vertices.append(vertex)
        elif isinstance(room_data, dict) and room_data.get('value') == room_number:
            vertices.append(vertex)
    return vertices

def find_room_by_vertex(data, coordinates):
    """Находит номер комнаты по координатам."""
    if len(data['point_b_to_a_map'][coordinates]) == 0:
        return 0
    else:
        return data['point_b_to_a_map'][coordinates][0]['value']

def draw_line(canvas, points, color='red'):
    """Отрисовка линии на холсте."""
    canvas.create_line(points, fill=color)


def merge_graphs(graph1, graph2, new_edges):
    """Объединяет два графа и добавляет новые рёбра."""
    merged_graph = nx.compose(graph1, graph2)
    for edge in new_edges:
        if edge[0] in merged_graph.nodes and edge[1] in merged_graph.nodes:
            merged_graph.add_edge(edge[0], edge[1])
    return merged_graph

# Пример использования

from PIL import Image, ImageTk
import json
import networkx as nx
import tkinter as tk

from matplotlib import pyplot as plt


def load_data_from_json(file_path):
    """Загрузка данных из JSON-файла."""
    with open(file_path, 'r') as f:
        return json.load(f)

def create_graph(data):
    """Создание графа из данных."""
    G = nx.Graph()
    prev_key = None
    first_key = None
    for key, value in data['point_b_to_a_map'].items():
        G.add_node(key)
        if first_key is None:
            first_key = key
        if prev_key is not None:
            G.add_edge(prev_key, key)
        prev_key = key
        if isinstance(value, list):
            for item in value:
                for k, v in item.items():
                    if k == "value":
                        v = str(v)
                        G.add_edge(key, v)
        elif isinstance(value, dict):
            for k, v in value.items():
                if k == "value":
                    v = str(v)
                    G.add_edge(key, v)
    if first_key is not None and prev_key is not None:
        G.add_edge(prev_key, first_key)
    return G

def find_vertex_by_room(data, room_number):
    """Находит вершины по номеру комнаты."""
    vertices = []
    for vertex, room_data in data['point_b_to_a_map'].items():
        if isinstance(room_data, list):
            for item in room_data:
                if isinstance(item, dict) and item.get('value') == room_number:
                    vertices.append(vertex)
                elif isinstance(item, list) and item[1] == room_number:
                    vertices.append(vertex)
        elif isinstance(room_data, dict) and room_data.get('value') == room_number:
            vertices.append(vertex)
    return vertices

def find_room_by_vertex(data, coordinates):
    """Находит номер комнаты по координатам."""
    if len(data['point_b_to_a_map'][coordinates]) == 0:
        return 0
    else:
        return data['point_b_to_a_map'][coordinates][0]['value']

def draw_line(canvas, points, color='red'):
    """Отрисовка линии на холсте."""
    canvas.create_line(points, fill=color)







def visualize_shortest_path(image_path, data_path):
    """Визуализация кратчайшего пути между двумя комнатами на изображении."""
    data = load_data_from_json(data_path)
    G = create_graph(data)

    root = tk.Tk()
    image = Image.open(image_path)
    image = image.resize((1000, 800))
    tk_image = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(root, width=1000, height=800, bg='white')
    canvas.create_image(0, 0, anchor='nw', image=tk_image)
    canvas.pack()
    root.geometry("1200x1000")

    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM)

    start_label = tk.Label(button_frame, text="Начальный кабинет:")
    start_label.pack(side=tk.TOP)
    start_entry = tk.Entry(button_frame)
    start_entry.pack(side=tk.TOP)

    target_label = tk.Label(button_frame, text="Конечный кабинет:")
    target_label.pack(side=tk.TOP)
    target_entry = tk.Entry(button_frame)
    target_entry.pack(side=tk.TOP)

    red_line_elements = []  # список для хранения элементов красной линии

    def visualize():
        nonlocal red_line_elements
        # Удаление предыдущей красной линии
        for element in red_line_elements:
            canvas.delete(element)
        red_line_elements = []  # очистка списка элементов

        start_room_number = start_entry.get()
        target_room_number = target_entry.get()
        start_room = find_vertex_by_room(data, start_room_number)[0]
        target_room = find_vertex_by_room(data, target_room_number)[0]
        shortest_path = nx.shortest_path(G, start_room, target_room)
        shortest_path_points = [(int(coord.split(',')[0][1:]), int(coord.split(',')[1][:-1])) for coord in shortest_path]
        red_line_elements = draw_line(canvas, shortest_path_points, color='red')

    visualize_button = tk.Button(button_frame, text="Визуализировать", command=visualize)
    visualize_button.pack(side=tk.BOTTOM)

    root.mainloop()
visualize_shortest_path('3.jpg', 'floor_plan3.json')
