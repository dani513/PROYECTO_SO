import os
import pandas as pd
import time
import csv

class ReproductorMusica:
    """
    Clase para representar un reproductor de música.

    Esta clase proporciona métodos para cargar, guardar y manipular una lista
    de reproducción de música.

    Atributos:
    playlist (DataFrame):
        DataFrame de pandas para almacenar la lista de reproducción.
    nombre_archivo (str):
        Nombre del archivo CSV donde se guarda la lista de reproducción.
    bloqueo (str):
        Nombre del archivo de bloqueo, para manejar el acceso concurrente a la lista de reproducción.
    """
    def __init__(self):
        """Inicializa la clase ReproductorMusica con una lista de reproducción vacía."""
        self.playlist = pd.DataFrame(columns=["Titulo", "Interprete", "Album",
                                              "Fecha", "Usuario", "Duracion"])
        
        self.nombre_archivo = "playlist.csv"  #archivo csv
        self.bloqueo = "bloqueo.txt"  #archivo de bloqueo
        
    def cargar_playlist(self):
        """Carga la lista de reproducción desde un archivo CSV.
            Si el archivo no existe, se imprime un mensaje de error.
        """
        try:
            self.playlist = pd.read_csv(self.nombre_archivo)
        except FileNotFoundError:
            print("El archivo no existe")

    def guardar_playlist(self):
        """Guarda la lista de reproduccion actual en el archivo csv.""" 
        self.playlist.to_csv(self.nombre_archivo, index=False)
        print("Agregada exitosamente a la playlist")

    def verificar_bloqueo(self):
        """
        Verifica si existe el archivo de bloqueo (bandera).
        Devuelve: 
        bool: True si el archivo de bloqueo existe, False en caso contrario.
        """
        return os.path.isfile(self.bloqueo)

    def crear_bloqueo(self):
        """Crea un archivo de bloqueo (bandera)."""
        with open(self.bloqueo, mode='w', newline='') as archivo_bloqueo:
            escritor = csv.writer(archivo_bloqueo)
            escritor.writerow(["En proceso"])

    def eliminar_bloqueo(self):
        """Elimina el archivo de bloqueo (bandera)."""
        os.remove(self.bloqueo)

    def agregar_cancion(self, titulo, interprete, album, fecha, usuario, duracion):
        """
        Agrega una canción a la lista de reproducción.
        Antes de agregar la canción, se verifica si ya está en la lista de reproducción.
        Si la canción ya está en la lista, se imprime un mensaje y no se agrega la canción.
        """
        self.cargar_playlist()  #carga la playlist desde CSV
        time.sleep(1)  
        
        if not self.playlist[(self.playlist['Titulo'] == titulo) & (self.playlist['Interprete'] == interprete)].empty:
            print(f"La canción '{titulo}' de '{interprete}' ya está en la playlist.")
            time.sleep(3)  
            self.eliminar_bloqueo()  #elimina archivo de bloqueo
            return
        
        nueva_cancion = pd.DataFrame([[titulo, interprete, album, fecha, usuario, duracion]],
                                      columns=["Titulo", "Interprete", "Album",
                                               "Fecha", "Usuario", "Duracion"])
        self.playlist = pd.concat([self.playlist, nueva_cancion], ignore_index=True)
        self.guardar_playlist()  #actualiza playlist
        time.sleep(2)
        self.eliminar_bloqueo()  

    def mostrar_playlist(self):
        """
        Muestra la lista de reproducción actual.
        Carga la lista de reproducción actual desde el archivo. Luego imprime la lista de reproducción completa
        y las dos últimas canciones agregadas.
        """
        self.cargar_playlist()
        ultimas_canciones = self.playlist.tail(2)
        print("Lista de Reproducción:") 
        print(self.playlist.to_string(index=False))
        print("\nÚltimas dos canciones agregadas:")
        print(ultimas_canciones.to_string(index=False))
        time.sleep(10)

if __name__ == "__main__":
    """Entrada principal del programa"""
    reproductor = ReproductorMusica()
    
    while True:
        
        os.system('clear')
        print("\nMenu:")
        print("[1]--> Agregar cancion")
        print("[2]--> Mostrar lista de reproduccion")
        print("[3]--> Salir")
        
        opcion = input("Seleccione una opcion: ")
        
        if opcion == "1":
            """Opción para agregar una canción a la lista de reproducción.
            Si la lista de reproducción está actualmente bloqueada (se está actualizando),
            se imprime un mensaje y se verifica repetidamente hasta que se desbloquee.
            Luego se solicita al usuario ingresar los detalles de la canción y se 
            agrega la canción a la lista de reproducción.
            """
            if reproductor.verificar_bloqueo(): #verifica el archivo bandera
                print("actualizacion de lista en curso, espere un momento.")
                while reproductor.verificar_bloqueo():
                    time.sleep(2)  
                    
            reproductor.crear_bloqueo()
            titulo = input("Título de la cancion: ")
            interprete = input("Interprete: ")
            album = input("Album: ")
            fecha = input("Fecha de agregacion: ")
            usuario = input("Usuario que agrego: ")
            duracion = input("Duracion: ")
            
            reproductor.agregar_cancion(titulo, interprete, album, fecha, usuario, duracion)
        
        elif opcion == "2":
            """Opción para mostrar la lista de reproducción actual."""
            reproductor.mostrar_playlist()  

        elif opcion == "3":
            """Opción para salir del programa."""
            break
        
        else:
            print("Opción no válida. Por favor, elija una opción del menú.")
            time.sleep(2)
