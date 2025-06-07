import customtkinter as ctk
import os
import subprocess
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Instalador desde PowerShell")
        self.geometry("700x550")

        self.ruta_script = "script.ps1"
        self.checkboxes = []  

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=650, height=400)
        self.scroll_frame.pack(pady=20)

        self.boton_ejecutar = ctk.CTkButton(self, text="Instalar seleccionados", command=self.ejecutar_comandos)
        self.boton_ejecutar.pack(pady=10)

        self.leer_archivo()

    def leer_archivo(self):
        if not os.path.exists(self.ruta_script):
            messagebox.showerror("Error", f"No se encontró el archivo: {self.ruta_script}")
            self.destroy()
            return

        with open(self.ruta_script, 'r', encoding='utf-8') as f:
            lineas = f.readlines()

        nombre_programa = None

        for linea in lineas:
            linea = linea.strip()

            if linea.startswith("#"):
               
                nombre_programa = linea[1:].strip()

            elif linea.lower().startswith("winget install"):
               
                if nombre_programa:
                    var = ctk.BooleanVar()
                    checkbox = ctk.CTkCheckBox(
                        self.scroll_frame,
                        text=nombre_programa,
                        variable=var
                    )
                    checkbox.pack(anchor="w", padx=10, pady=3)
                    self.checkboxes.append((nombre_programa, linea, var))
                    nombre_programa = None  

    def ejecutar_comandos(self):
        comandos_seleccionados = [comando for _, comando, var in self.checkboxes if var.get()]

        if not comandos_seleccionados:
            messagebox.showinfo("Aviso", "No se seleccionó ningún programa.")
            return

        for cmd in comandos_seleccionados:
            print(f"Ejecutando: {cmd}")
            try:
                subprocess.run(["powershell", "-Command", cmd], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error ejecutando '{cmd}':", e)
                messagebox.showerror("Error", f"Falló la instalación:\n{cmd}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
