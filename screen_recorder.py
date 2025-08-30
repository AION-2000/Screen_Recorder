import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import pyautogui
import threading
import time

class ScreenRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder")
        self.root.geometry("300x150")
        
        # Recording state
        self.recording = False
        self.video_writer = None
        self.output_file = None
        
        # GUI Elements
        self.label = tk.Label(root, text="Press 'Start Recording' to begin")
        self.label.pack(pady=10)
        
        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=5)
        
        self.select_button = tk.Button(root, text="Select Output Path", command=self.select_output_path)
        self.select_button.pack(pady=5)
        
        self.output_path = "screen_record.avi"  # Default path

    def select_output_path(self):
        """Dialog to choose output file path"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".avi",
            filetypes=[("AVI files", "*.avi"), ("All files", "*.*")]
        )
        if file_path:
            self.output_path = file_path
            self.label.config(text=f"Output: {file_path}")

    def start_recording(self):
        """Start screen recording in a separate thread"""
        if not self.output_path:
            messagebox.showwarning("Warning", "Please select an output path first!")
            return
            
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.label.config(text="Recording... Press 'Stop' to finish")
        
        # Start recording in a new thread to avoid freezing the GUI
        threading.Thread(target=self._record_screen, daemon=True).start()

    def _record_screen(self):
        """Core recording logic (runs in a separate thread)"""
        try:
            # Get screen dimensions
            screen_width, screen_height = pyautogui.size()
            
            # Define codec and create VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            self.video_writer = cv2.VideoWriter(
                self.output_path, 
                fourcc, 
                20.0,  # FPS
                (screen_width, screen_height)
            )
            
            while self.recording:
                # Capture screen
                screenshot = pyautogui.screenshot()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Write frame to video
                self.video_writer.write(frame)
                time.sleep(0.05)  # Control FPS (20 FPS = 0.05s delay)
                
        except Exception as e:
            messagebox.showerror("Error", f"Recording failed: {str(e)}")
        finally:
            if self.video_writer:
                self.video_writer.release()

    def stop_recording(self):
        """Stop recording and reset GUI"""
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.label.config(text=f"Recording saved to:\n{self.output_path}")
        messagebox.showinfo("Success", "Recording saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorder(root)
    root.mainloop()