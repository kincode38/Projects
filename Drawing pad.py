import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
import json
import os

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Pad - Enhanced")
        self.root.geometry("900x750")
        self.root.configure(bg="#f0f0f0")
        
        # Drawing state
        self.current_color = "black"
        self.current_thickness = 2
        self.current_tool = "pencil"
        self.fill_enabled = False
        self.start_x = None
        self.start_y = None
        self.preview_shape_id = None
        
        # History for undo/redo
        self.drawing_history = []
        self.history_index = -1
        
        self.setup_ui()
        self.save_state()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Canvas
        self.canvas = tk.Canvas(self.root, width=800, height=500, bg="white", 
                               relief="ridge", bd=2, cursor="crosshair")
        self.canvas.pack(pady=10, padx=10)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        # Control frame
        control_frame = tk.Frame(self.root, bg="#d9d9d9", pady=10)
        control_frame.pack(fill="x", padx=10)
        
        # Color button
        self.color_button = tk.Button(control_frame, text="Color", bg=self.current_color, 
                                     fg="white", command=self.set_color, width=10)
        self.color_button.grid(row=0, column=0, padx=5)
        
        # Clear button
        clear_button = tk.Button(control_frame, text="Clear", bg="#f44336", fg="white",
                                command=self.clear_canvas, width=10)
        clear_button.grid(row=0, column=1, padx=5)
        
        # Undo/Redo buttons
        undo_button = tk.Button(control_frame, text="Undo", bg="#2196F3", fg="white",
                               command=self.undo, width=8)
        undo_button.grid(row=0, column=2, padx=2)
        
        redo_button = tk.Button(control_frame, text="Redo", bg="#2196F3", fg="white",
                               command=self.redo, width=8)
        redo_button.grid(row=0, column=3, padx=2)
        
        # Save/Load buttons
        save_button = tk.Button(control_frame, text="Save", bg="#4CAF50", fg="white",
                               command=self.save_drawing, width=8)
        save_button.grid(row=0, column=4, padx=2)
        
        load_button = tk.Button(control_frame, text="Load", bg="#4CAF50", fg="white",
                               command=self.load_drawing, width=8)
        load_button.grid(row=0, column=5, padx=2)
        
        # Thickness control
        thickness_label = tk.Label(control_frame, text="Thickness", bg="#d9d9d9")
        thickness_label.grid(row=0, column=6, padx=5)
        
        self.thickness_slider = tk.Scale(control_frame, from_=1, to=30, orient="horizontal",
                                        command=self.change_thickness, bg="#d9d9d9", length=100)
        self.thickness_slider.set(self.current_thickness)
        self.thickness_slider.grid(row=0, column=7, padx=5)
        
        # Fill toggle
        self.fill_button = tk.Button(control_frame, text="Fill: OFF", bg="#FF9800", fg="white",
                                    command=self.toggle_fill, width=8)
        self.fill_button.grid(row=0, column=8, padx=2)
        
        # Tool selection frame
        tool_frame = tk.Frame(self.root, bg="#f0f0f0")
        tool_frame.pack(fill="x", padx=10, pady=5)
        
        shape_label = tk.Label(tool_frame, text="Tools:", bg="#f0f0f0", font=("Arial", 10, "bold"))
        shape_label.pack(side="left", padx=5)
        
        self.tool_buttons = {}
        tools = ["pencil", "eraser", "line", "rectangle", "oval"]
        
        for tool in tools:
            btn = tk.Button(tool_frame, text=tool.capitalize(), 
                          command=lambda t=tool: self.set_tool(t), width=10,
                          bg="#E0E0E0")
            btn.pack(side="left", padx=2)
            self.tool_buttons[tool] = btn
        
        # Status label
        self.tool_label = tk.Label(self.root, text=f"Tool: Pencil | Color: Black | Thickness: 2", 
                                  bg="#f0f0f0", font=("Arial", 10))
        self.tool_label.pack(pady=5)
        
        # Keyboard shortcuts info
        info_label = tk.Label(self.root, text="Shortcuts: Ctrl+Z (Undo) | Ctrl+Y (Redo) | Ctrl+S (Save) | Ctrl+L (Load)",
                            bg="#f0f0f0", font=("Arial", 8), fg="#666666")
        info_label.pack(pady=2)
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-s>", lambda e: self.save_drawing())
        self.root.bind("<Control-l>", lambda e: self.load_drawing())
        
        self.update_tool_button_states()
    
    def set_tool(self, tool):
        """Set the current drawing tool"""
        self.current_tool = tool
        self.update_tool_button_states()
        self.update_status_label()
    
    def update_tool_button_states(self):
        """Highlight the active tool button"""
        for tool, btn in self.tool_buttons.items():
            if tool == self.current_tool:
                btn.config(bg="#4CAF50", fg="white")
            else:
                btn.config(bg="#E0E0E0", fg="black")
    
    def set_color(self):
        """Open color chooser dialog"""
        color = colorchooser.askcolor(title="Choose drawing color", color=self.current_color)
        if color[1]:
            self.current_color = color[1]
            # Adjust text color based on background brightness
            brightness = sum(int(self.current_color[i:i+2], 16) for i in (1, 3, 5)) / 3
            text_color = "white" if brightness < 128 else "black"
            self.color_button.config(bg=self.current_color, fg=text_color)
            self.update_status_label()
    
    def change_thickness(self, value):
        """Change drawing thickness"""
        self.current_thickness = int(value)
        self.update_status_label()
    
    def toggle_fill(self):
        """Toggle fill for shapes"""
        self.fill_enabled = not self.fill_enabled
        status = "ON" if self.fill_enabled else "OFF"
        self.fill_button.config(text=f"Fill: {status}")
        self.update_status_label()
    
    def update_status_label(self):
        """Update the status label with current settings"""
        fill_status = f" | Fill: {'ON' if self.fill_enabled else 'OFF'}"
        self.tool_label.config(
            text=f"Tool: {self.current_tool.capitalize()} | Color: {self.current_color} | "
                 f"Thickness: {self.current_thickness}{fill_status}"
        )
    
    def clear_canvas(self):
        """Clear the canvas"""
        if messagebox.askyesno("Clear Canvas", "Are you sure you want to clear the canvas?"):
            self.canvas.delete("all")
            self.save_state()
    
    def save_state(self):
        """Save current canvas state to history"""
        # Store PostScript representation
        try:
            state = self.canvas.postscript()
            self.history_index += 1
            self.drawing_history = self.drawing_history[:self.history_index]
            self.drawing_history.append(state)
        except:
            pass
    
    def undo(self):
        """Undo last action"""
        if self.history_index > 0:
            self.history_index -= 1
            self.restore_state()
    
    def redo(self):
        """Redo last undone action"""
        if self.history_index < len(self.drawing_history) - 1:
            self.history_index += 1
            self.restore_state()
    
    def restore_state(self):
        """Restore canvas to a specific history state"""
        if 0 <= self.history_index < len(self.drawing_history):
            self.canvas.delete("all")
            try:
                # Draw using the stored PostScript
                self.canvas.eval(self.drawing_history[self.history_index])
            except:
                # Fallback: just clear if PostScript doesn't work
                pass
    
    def save_drawing(self):
        """Save drawing to file"""
        file = filedialog.asksaveasfilename(
            defaultextension=".ps",
            filetypes=[("PostScript", "*.ps"), ("All Files", "*.*")]
        )
        if file:
            try:
                self.canvas.postscript(file=file)
                messagebox.showinfo("Success", f"Drawing saved to {os.path.basename(file)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save drawing: {str(e)}")
    
    def load_drawing(self):
        """Load drawing from file"""
        file = filedialog.askopenfilename(
            filetypes=[("PostScript", "*.ps"), ("All Files", "*.*")]
        )
        if file:
            try:
                self.canvas.delete("all")
                # Read PostScript file
                with open(file, 'r') as f:
                    postscript = f.read()
                self.canvas.eval(postscript)
                self.save_state()
                messagebox.showinfo("Success", f"Drawing loaded from {os.path.basename(file)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load drawing: {str(e)}")
    
    def on_button_press(self, event):
        """Handle mouse button press"""
        self.start_x, self.start_y = event.x, event.y
        
        if self.current_tool == "pencil":
            self.canvas.create_oval(
                self.start_x - self.current_thickness, self.start_y - self.current_thickness,
                self.start_x + self.current_thickness, self.start_y + self.current_thickness,
                fill=self.current_color, outline=self.current_color
            )
        elif self.current_tool == "eraser":
            self.canvas.create_oval(
                self.start_x - self.current_thickness, self.start_y - self.current_thickness,
                self.start_x + self.current_thickness, self.start_y + self.current_thickness,
                fill="white", outline="white"
            )
    
    def on_move(self, event):
        """Handle mouse motion"""
        if self.current_tool == "pencil":
            x, y = event.x, event.y
            self.canvas.create_line(self.start_x, self.start_y, x, y,
                                   fill=self.current_color, width=self.current_thickness,
                                   capstyle=tk.ROUND, smooth=True)
            self.start_x, self.start_y = x, y
        
        elif self.current_tool == "eraser":
            x, y = event.x, event.y
            self.canvas.create_oval(
                x - self.current_thickness, y - self.current_thickness,
                x + self.current_thickness, y + self.current_thickness,
                fill="white", outline="white"
            )
            self.start_x, self.start_y = x, y
        
        else:
            # Preview for shapes
            if self.preview_shape_id:
                self.canvas.delete(self.preview_shape_id)
            
            x, y = event.x, event.y
            
            if self.current_tool == "line":
                self.preview_shape_id = self.canvas.create_line(
                    self.start_x, self.start_y, x, y,
                    fill=self.current_color, width=self.current_thickness
                )
            elif self.current_tool == "rectangle":
                self.preview_shape_id = self.canvas.create_rectangle(
                    self.start_x, self.start_y, x, y,
                    outline=self.current_color, fill="" if not self.fill_enabled else self.current_color,
                    width=self.current_thickness
                )
            elif self.current_tool == "oval":
                self.preview_shape_id = self.canvas.create_oval(
                    self.start_x, self.start_y, x, y,
                    outline=self.current_color, fill="" if not self.fill_enabled else self.current_color,
                    width=self.current_thickness
                )
    
    def on_button_release(self, event):
        """Handle mouse button release"""
        if self.current_tool in ("line", "rectangle", "oval"):
            x, y = event.x, event.y
            
            if self.preview_shape_id:
                self.canvas.delete(self.preview_shape_id)
                self.preview_shape_id = None
            
            if self.current_tool == "line":
                self.canvas.create_line(self.start_x, self.start_y, x, y,
                                       fill=self.current_color, width=self.current_thickness)
            elif self.current_tool == "rectangle":
                self.canvas.create_rectangle(self.start_x, self.start_y, x, y,
                                           outline=self.current_color, 
                                           fill="" if not self.fill_enabled else self.current_color,
                                           width=self.current_thickness)
            elif self.current_tool == "oval":
                self.canvas.create_oval(self.start_x, self.start_y, x, y,
                                       outline=self.current_color,
                                       fill="" if not self.fill_enabled else self.current_color,
                                       width=self.current_thickness)
            
            self.save_state()


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
