from file import *
from upload import upload_file
import tkinter as tk
from tkinter import *

def main():
    root = tk.Tk()
    root.title("Convertir fichier")
    root.geometry("800x500+500+100")

    def handle_upload():
        filename = upload_file()
        if filename:
            file_format = detect_file_format(filename)
            if file_format:
                print(f"Format détecté: {file_format}")

                # Exemple: Lire le contenu du fichier
                data = read_file(filename, file_format)

                # Exemple: Convertir les données dans un autre format
                new_format = input("Veuillez entrer le format de conversion (csv, json, xml, yaml): ")
                if new_format in ["csv", "json", "xml", "yaml"]:
                    converted_data = convert_data(data, new_format)
                    print(f"Données converties au format {new_format}: {converted_data}")
                else:
                    print("Format de conversion invalide.")

                # Exemple: Vérifier les données (s'il y a une fonction de vérification)

            else:
                print("Format indisponible.")
        else:
            print("Aucun fichier sélectionné.")

    button_upload = tk.Button(root, text="Télécharger un fichier", command=handle_upload)
    button_upload.pack(padx=50 ,pady=50)

    detect_format = tk.Label(root, text="")
    detect_format.pack(padx=50)
    root.mainloop()

if __name__ == "__main__":
    main()
