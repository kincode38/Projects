import tkinter as tk
from tkinter import colorchooser

root = tk.Tk()
root.title("Drawing pad")
root.geometry("800x650")
root.configure(bg="#f0f0f0")

current_color = "black"
current_thickness = 2
current_tool = "pencil"
start_x = None
start_y = None
preview_shape_id = None

canvas = tk.Canvas(root, width=700, height=500, bg="white", relief="ridge", bd=2)
canvas.pack(pady=10)


def set_tool(tool):
    global current_tool
    current_tool = tool
    tool_label.config(text=f"Tool: {tool.capitalize()}")


def set_color():
    global current_color
    color = colorchooser.askcolor(title="Choose drawing color")
    if color[1]:
        current_color = color[1]
        color_button.config(bg=current_color)


def change_thickness(value):
    global current_thickness
    current_thickness = int(value)


def clear_canvas():
    canvas.delete("all")


def on_button_press(event):
    global start_x, start_y, preview_shape_id
    start_x, start_y = event.x, event.y
    if current_tool == "pencil":
        canvas.create_oval(
            start_x - current_thickness, start_y - current_thickness,
            start_x + current_thickness, start_y + current_thickness,
            fill=current_color, outline=current_color
        )


def on_move(event):
    global start_x, start_y, preview_shape_id
    if current_tool == "pencil":
        x, y = event.x, event.y
        canvas.create_line(start_x, start_y, x, y,
                           fill=current_color, width=current_thickness,
                           capstyle=tk.ROUND, smooth=True)
        start_x, start_y = x, y
    else:
        if preview_shape_id:
            canvas.delete(preview_shape_id)
        x, y = event.x, event.y
        if current_tool == "line":
            preview_shape_id = canvas.create_line(start_x, start_y, x, y,
                                                  fill=current_color, width=current_thickness)
        elif current_tool == "rectangle":
            preview_shape_id = canvas.create_rectangle(start_x, start_y, x, y,
                                                       outline=current_color,
                                                       width=current_thickness)
        elif current_tool == "oval":
            preview_shape_id = canvas.create_oval(start_x, start_y, x, y,
                                                  outline=current_color,
                                                  width=current_thickness)


def on_button_release(event):
    global preview_shape_id
    if current_tool in ("line", "rectangle", "oval"):
        x, y = event.x, event.y
        if preview_shape_id:
            canvas.delete(preview_shape_id)
            preview_shape_id = None

        if current_tool == "line":
            canvas.create_line(start_x, start_y, x, y,
                               fill=current_color, width=current_thickness)
        elif current_tool == "rectangle":
            canvas.create_rectangle(start_x, start_y, x, y,
                                    outline=current_color, width=current_thickness)
        elif current_tool == "oval":
            canvas.create_oval(start_x, start_y, x, y,
                               outline=current_color, width=current_thickness)


canvas.bind("<ButtonPress-1>", on_button_press)
canvas.bind("<B1-Motion>", on_move)
canvas.bind("<ButtonRelease-1>", on_button_release)

control_frame = tk.Frame(root, bg="#d9d9d9", pady=10)
control_frame.pack(fill="x", padx=10)

color_button = tk.Button(control_frame, text="Color", bg=current_color, fg="white",
                         command=set_color, width=10)
color_button.grid(row=0, column=0, padx=5)

clear_button = tk.Button(control_frame, text="Clear", bg="#f44336", fg="white",
                         command=clear_canvas, width=10)
clear_button.grid(row=0, column=1, padx=5)

thickness_label = tk.Label(control_frame, text="Thickness", bg="#d9d9d9")
thickness_label.grid(row=0, column=2, padx=5)

thickness_slider = tk.Scale(control_frame, from_=1, to=20, orient="horizontal",
                            command=change_thickness, bg="#d9d9d9")
thickness_slider.set(current_thickness)
thickness_slider.grid(row=0, column=3, padx=5)

shape_label = tk.Label(control_frame, text="Shapes", bg="#d9d9d9")
shape_label.grid(row=0, column=4, padx=5)

pencil_btn = tk.Button(control_frame, text="Pencil", command=lambda: set_tool("pencil"))
pencil_btn.grid(row=0, column=5, padx=2)

line_btn = tk.Button(control_frame, text="Line", command=lambda: set_tool("line"))
line_btn.grid(row=0, column=6, padx=2)

rect_btn = tk.Button(control_frame, text="Rectangle", command=lambda: set_tool("rectangle"))
rect_btn.grid(row=0, column=7, padx=2)

oval_btn = tk.Button(control_frame, text="Oval", command=lambda: set_tool("oval"))
oval_btn.grid(row=0, column=8, padx=2)

tool_label = tk.Label(root, text=f"Tool: {current_tool.capitalize()}", bg="#f0f0f0", font=("Arial", 11, "bold"))
tool_label.pack(pady=5)

root.mainloop()