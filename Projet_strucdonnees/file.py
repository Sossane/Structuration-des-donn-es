
                                                        #Importation des bibliothéques
import csv
import xml.etree.ElementTree as ET
import yaml
import json
import os
import tkinter as tk
import tkinter as ttk
from tkinter import filedialog                                                   

 #Fonction pour détecter le type de fichier

def detect_file_format(fichier):
    """Détecte le format d'un fichier en fonction de son extension.

    Args:
        fichier (str): Le nom du fichier (incluant l'extension) à détecter.

    Returns:
        module: Le module approprié pour gérer le format détecté (par exemple csv, json, xml, yaml),
                ou None si le format n'est pas supporté.

    Raises:
        ImportError: Si un module importé est introuvable (bibliothèque potentiellement manquante).
    """
    extension = os.path.splitext(fichier)[1].lower()
    supported_formats = {
        ".csv": "csv",
        ".json": "json",
        ".xml": "xml",
        ".yaml": "yaml",
    }
    if extension in supported_formats:
        return supported_formats[extension]
    else:
        return None

                                                    #Fonction pour lire les fichiers 
def read_file(filename, format):
    """Lit le contenu d'un fichier en fonction de son format.

    Args:
        filename (str): Le nom du fichier à lire.
        format (str): Le format du fichier (par exemple "csv", "json", "xml", "yaml", "xsl").

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
   
                                                        #Fonction pour la conversion des fichiers
def convert_data(data, new_format):
    """Convertit les données d'un format à un autre.

    Args:
        data: Les données à convertir (type dépend du format d'origine).
        new_format (str): Le nouveau format de fichier souhaité (par exemple "csv", "json", "xml", "yaml", "xsl").

    Returns:
        any: Les données converties au nouveau format, le type de données dépend du nouveau format.
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


#Fonction ouvre une boîte de dialogue pour sélectionner le fichier 
def upload_file():
    filename = filedialog.askopenfilename(title="Sélectionner un fichier", filetypes=(("Fichiers CSV", "*.csv"),
                                                                                      ("Fichiers JSON", "*.json"),
                                                                                      ("Fichiers XML", "*.xml"),
                                                                                      ("Fichiers YAML", "*.yaml"),
                                                                                      ("Tous les fichiers", "*.*")))
    return filename

#Fonction main   
def main():
    root = tk.Tk()
    root.title("Structuration de données fichier")
    root.geometry("800x500+500+100")

    def handle_upload_and_convert():
        filename = upload_file()
        selected_format = format_var.get()

        if filename:
            file_format = detect_file_format(filename)
            if file_format:
                detect_format.config(text=f"Format détecté: {file_format}")

                try:
                    data = read_file(filename, file_format)
                    if selected_format in ["csv", "json", "xml", "yaml"]:
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

    button_upload = tk.Button(root, text="Télécharger un fichier et convertir", command=handle_upload_and_convert)
    button_upload.pack(padx=50 ,pady=50)

    detect_format = tk.Label(root, text="")
    detect_format.pack(padx=50)

    format_var = tk.StringVar()
    format_var.set("Choisir un format de conversion")
    convert_format = ttk.OptionMenu(root, format_var, "csv", "json", "xml", "yaml")
    convert_format.pack(padx=100, pady=50)

    root.mainloop()

if __name__ == "__main__":
    main()
