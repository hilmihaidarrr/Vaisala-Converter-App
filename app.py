import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel, Label
import txt_to_csv  # Import your previous script
import threading

def select_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("TXT Files", "*.txt"), ("All Files", "*.*")])
    if file_paths:
        file_paths = list(file_paths)  # Convert tuple to list
        process_files(file_paths)

def process_files(file_paths):
    def process_next_file():
        if file_paths:
            file_path = file_paths.pop(0)
            try:
                # Show loading popup
                show_loading_popup()
                
                # Process file in a separate thread to keep the GUI responsive
                threading.Thread(target=process_file, args=(file_path, process_next_file)).start()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while processing {file_path}: {str(e)}")
        else:
            # All files processed, show success message
            root.after(0, lambda: messagebox.showinfo("Success", "Semua file berhasil diubah!!"))

    process_next_file()

def process_file(file_path, callback):
    try:
        processed_file = txt_to_csv.process_txt(file_path)
    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Error", f"An error occurred while processing {file_path}: {str(e)}"))
    finally:
        # Close loading popup in the main thread
        root.after(0, close_loading_popup)
        root.after(0, callback)

def show_loading_popup():
    global loading_popup
    loading_popup = Toplevel(root)
    loading_popup.title("Loading")
    loading_popup.geometry("200x100")
    Label(loading_popup, text="Processing... Please wait").pack(pady=20)
    loading_popup.transient(root)
    loading_popup.grab_set()

def close_loading_popup():
    global loading_popup
    if loading_popup:
        loading_popup.destroy()
        loading_popup = None

# Setup GUI
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

root = ctk.CTk()  # Use CTk 
root.title("Vaisala Data Converter")
root.geometry("600x400")

# Create a frame with black background
frame = ctk.CTkFrame(root, fg_color='#1a1a1a')
frame.place(relwidth=1, relheight=1)

label_frame = ctk.CTkFrame(frame, fg_color='#1a1a1a')
label_frame.pack(expand=True, pady=60)

label = ctk.CTkLabel(label_frame, text="Pilih TXT file untuk dikonversi menjadi CSV", font=('Helvetica', 20, 'bold'), text_color='white')
label.pack(pady=10)

button = ctk.CTkButton(label_frame, text="Pilih File", command=select_files, font=('Helvetica', 16), fg_color='#0080FF', text_color='white', corner_radius=10, width=200, height=50)
button.pack(pady=10)

label2 = ctk.CTkLabel(label_frame, text="File akan disimpan di lokasi yang sama dengan format nama (nama file awal + _formatted.csv)", font=('Helvetica', 12), text_color='gray')
label2.pack(pady=10)

footer_label = ctk.CTkLabel(frame, text="Dibuat oleh Hilmi dan Nabila", font=('Helvetica', 12), text_color='gray')
footer_label.pack(side='bottom', pady=20)

root.mainloop()
