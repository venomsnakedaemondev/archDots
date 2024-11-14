from tqdm import tqdm
def mostrar_barra_carga(total_paquetes):
    """Muestra una barra de progreso mientras se instalan los paquetes."""
    with tqdm(total=total_paquetes, desc="Instalando paquetes", unit="paquete", ncols=100, dynamic_ncols=True, ascii=True) as barra:
        # La barra se actualiza en cada paquete que se instala
        for i in range(total_paquetes):
            barra.update(1)