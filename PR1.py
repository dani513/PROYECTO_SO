import pandas as pd

class ReproductorMusica:
    def __init__(self):
        self.playlist = pd.DataFrame(columns=["Título", "Intérprete", "Álbum", "Fecha", "Usuario", "Duración"])
        self.nombre_archivo = "playlist.csv"  # Nombre del archivo CSV
        
    def cargar_playlist(self):
        try:
            self.playlist = pd.read_csv(self.nombre_archivo)
        except FileNotFoundError:
            print("El archivo de playlist aún no existe. Se creará al agregar canciones.")

    def guardar_playlist(self):
        self.playlist.to_csv(self.nombre_archivo, index=False)

    def agregar_cancion(self, titulo, interprete, album, fecha, usuario, duracion):
        self.cargar_playlist()  # Cargar la playlist actual desde el archivo
        # Verificar si la canción ya está en la lista
        if not self.playlist[(self.playlist['Título'] == titulo) & (self.playlist['Intérprete'] == interprete)].empty:
            print(f"La canción '{titulo}' de '{interprete}' ya está en la lista.")
            return
        
        nueva_cancion = pd.DataFrame([[titulo, interprete, album, fecha, usuario, duracion]],
                                      columns=["Título", "Intérprete", "Álbum", "Fecha", "Usuario", "Duración"])
        self.playlist = pd.concat([self.playlist, nueva_cancion], ignore_index=True)
        self.guardar_playlist()  # Guardar la playlist actualizada en el archivo
    
    def mostrar_playlist(self):
        self.cargar_playlist()  # Cargar la playlist actual desde el archivo
        # Mostrar las dos últimas canciones agregadas
        ultimas_canciones = self.playlist.tail(2)
        print("Lista de Reproducción:")
        print(self.playlist.to_string(index=False))
        print("\nÚltimas dos canciones agregadas:")
        print(ultimas_canciones.to_string(index=False))

# Ejemplo de uso
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
