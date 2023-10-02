import os
import pandas as pd
import time

class ReproductorMusica:  #Clase Reproductor de musica 
    def __init__(self): #constructor 
        #Inicializar la lista como un DataFrame vacio 
        self.playlist = pd.DataFrame(columns=["Titulo", "Interprete", "Album",
                                              "Fecha", "Usuario", "Duracion"])
        
        self.nombre_archivo = "playlist.csv"  #archivo csv
        self.bloqueo = "bloqueo.txt"  #archivo de bloqueo (bandera)
        
##############################################################################
    def cargar_playlist(self): #Carga la lista desde el archivo csv
        try:
            self.playlist = pd.read_csv(self.nombre_archivo)
        except FileNotFoundError:
            print("El archivo no existe")


##############################################################################
    def guardar_playlist(self): #guarda la lista de reproduccion actual en el csv 
        self.playlist.to_csv(self.nombre_archivo, index=False)


##############################################################################
    def verificar_bloqueo(self): #verifica el si existe el archivo bandera
        return os.path.isfile(self.bloqueo)


##############################################################################
    def crear_bloqueo(self): #crea archivo bandera
        with open(self.bloqueo, "w") as f:
            pass


##############################################################################
    def eliminar_bloqueo(self): #elimina el archivo bandera
        os.remove(self.bloqueo)


##############################################################################
    def agregar_cancion(self, titulo, interprete, album, fecha, usuario, duracion):
        self.cargar_playlist()  #carga la playlist actual desde el archivo csv
        if self.verificar_bloqueo(): #verifica el archivo bandera
            print("actualizacion de lista en curso, espere un momento.")
            while self.verificar_bloqueo():
                time.sleep(1)
        
        self.crear_bloqueo()  #Crear archivo de bloqueo
        # Verificar si la canción ya está en la lista
        if not self.playlist[(self.playlist['Titulo'] == titulo) & (self.playlist['Interprete'] == interprete)].empty:
            print(f"La canción '{titulo}' de '{interprete}' ya está en la playlist.")
            self.eliminar_bloqueo()  # elimina archivo de bloqueo
            return
        
        nueva_cancion = pd.DataFrame([[titulo, interprete, album, fecha, usuario, duracion]],
                                      columns=["Titulo", "Interprete", "Album",
                                               "Fecha", "Usuario", "Duración"])
        self.playlist = pd.concat([self.playlist, nueva_cancion], ignore_index=True)
        self.guardar_playlist()  #guarda la playlist actualizada en el archivo
        self.eliminar_bloqueo()  


##############################################################################
    def mostrar_playlist(self):
        self.cargar_playlist()  #carga la playlist actual desde el csv
        # Mostrar las dos últimas canciones agregadas
        ultimas_canciones = self.playlist.tail(2)
        print("Lista de Reproducción:") # OJO BORRAR 
        print(self.playlist.to_string(index=False))
        print("\nÚltimas dos canciones agregadas:")
        print(ultimas_canciones.to_string(index=False))


##############################################################################

if __name__ == "__main__":
    reproductor = ReproductorMusica()

    while True:
        print("\nMenú:")
        print("1. Agregar canción")
        print("2. Mostrar lista de reproducción")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            titulo = input("Título de la canción: ")
            interprete = input("Intérprete: ")
            album = input("Álbum: ")
            fecha = input("Fecha de agregación: ")
            usuario = input("Usuario que agregó: ")
            duracion = input("Duración: ")
            
            reproductor.agregar_cancion(titulo, interprete, album, fecha, usuario, duracion)
        
        elif opcion == "2":
            reproductor.mostrar_playlist()
        
        elif opcion == "3":
            break
