import tkinter as tk
from tkinter import ttk
import customtkinter
import tkinter as tk
from tkinter import filedialog  
import tkinter as ttk
from file import *

# Fonction pour détecter le type de fichier
def detect_file_format(fichier):
    """Détecte le format d'un fichier en fonction de son extension.

    Args:
        fichier (str): Le nom du fichier (incluant l'extension) à détecter.

    Returns:
        str: Le format détecté (par exemple csv, json, xml, yaml), ou None si le format n'est pas supporté.
    """
    extension = os.path.splitext(fichier)[1].lower()
    supported_formats = {
        ".csv": "csv",
        ".json": "json",
        ".xml": "xml",
        ".yaml": "yaml",
    }
    return supported_formats.get(extension)

# Fonction pour lire les fichiers
def read_file(filename, format):
    """Lit le contenu d'un fichier en fonction de son format.

    Args:
        filename (str): Le nom du fichier à lire.
        format (str): Le format du fichier (par exemple "csv", "json", "xml", "yaml").

    Returns:
        any: Le contenu du fichier lu, le type de données dépend du format du fichier.
    """
    if format == "csv":
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return data
    elif format == "json":
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    elif format == "xml":
        tree = ET.parse(filename)
        root = tree.getroot()
        data = []
        for element in root:
            data.append(element)
        return data
    elif format == "yaml":
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
        return data
    else:
        raise ValueError(f"Format de fichier inconnu: {format}")

# Fonction pour la conversion des fichiers
def convert_data(data, new_format):
    """Convertit les données d'un format à un autre.

    Args:
        data: Les données à convertir (type dépend du format d'origine).
        new_format (str): Le nouveau format de fichier souhaité (par exemple "csv", "json", "xml", "yaml").

    Returns:
        str: Le nom du fichier converti.
    """
    if new_format == "csv":
        with open('converted_data.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return "converted_data.csv"
    elif new_format == "json":
        with open('converted_data.json', 'w') as f:
            json.dump(data, f, indent=4)
        return "converted_data.json"
    elif new_format == "xml":
        root = ET.Element("data")
        for item in data:
            element = ET.SubElement(root, "item")
            for key, value in item.items():
                element.set(key, value)
        tree = ET.tostring(root, encoding="utf-8")
        with open('converted_data.xml', 'wb') as f:
            f.write(tree)
        return "converted_data.xml"
    elif new_format == "yaml":
        with open('converted_data.yaml', 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        return "converted_data.yaml"
    else:
        raise ValueError(f"Format de fichier inconnu: {new_format}")
def main():
    root = tk.Tk()
    root.title("Structuration de données fichier")
    root.geometry("500x300")

    def handle_upload_and_convert():
        filename = upload_file()
        selected_format = format_var.get()

        if filename:
            file_format = detect_file_format(filename)
            if file_format:
                detect_format.config(text=f"Format détecté: {file_format}")

                try:
                    data = read_file(filename, file_format)
                    if selected_format in ["CSV", "JSON", "XML", "YAML"]:
                        converted_data = convert_data(data, selected_format)
                        print(f"Données converties au format {selected_format}: {converted_data}")
                    else:
                        print("Format de conversion invalide.")
                except Exception as e:
                    print(f"Erreur lors du traitement du fichier: {e}")
            else:
                print("Format indisponible.")
        else:
            print("Aucun fichier sélectionné.")

    
    frame = ttk.Frame(root, padx="20")
    frame.pack(expand=True, fill='both')

    label = ttk.Label(frame, text="Sélectionner un fichier et un format de conversion")
    label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    button_upload = ttk.Button(frame, text="Télécharger un fichier", command=handle_upload_and_convert)
    button_upload.grid(row=1, column=0, pady=10)

    format_var = tk.StringVar()
    format_var.set("CSV")
    convert_format = ttk.OptionMenu(frame, format_var, "CSV", "JSON", "XML", "YAML")
    convert_format.grid(row=1, column=1, pady=10)

    detect_format = ttk.Label(frame, text="")
    detect_format.grid(row=2, column=0, columnspan=2)        

    button_convert = ttk.Button(frame, text="Convertir", command=handle_upload_and_convert)
    button_convert.grid(row=3, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()



"""def handle_selection(event):
    selected_item = combo_box.get()
    print("Élément sélectionné :", selected_item)

root = tk.Tk()
root.title("Liste déroulante Tkinter")
root.geometry("300x200")

# Options pour la liste déroulante
options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]

# Créer une liste déroulante
combo_box = ttk.Combobox(root, values=options)
combo_box.pack(pady=20)
combo_box.current(0)  # Sélectionner l'élément par défaut

# Lier une fonction à l'événement de sélection
combo_box.bind("<<ComboboxSelected>>", handle_selection)

root.mainloop()"""
