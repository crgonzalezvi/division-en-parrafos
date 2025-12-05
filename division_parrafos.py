"""
Proyecto: División en Párrafos
Análisis y Diseño de Algoritmos
Implementaciones: Iterativa, Recursiva, Divide y Vencerás, Exhaustiva
Autores: Cristian Camilo González Villa , José David López Ostos
"""

import time
#Para medición de tiempo de ejecución
from typing import List, Tuple, Dict
#Facilitar la manipulación de argumentos y salida del sistema
import sys
#Inreaccion con el SO


TIEMPO_UMBRAL_LENTO = 30.0  # segundos
# Tiempo "limite" para considerar un algoritmo como lento

class DivisionParrafos:
    """Clase principal para resolver el problema de División en Párrafos"""
    
    def __init__(self, palabras: List[int], L: int, b: float):
        """
        Args:
            palabras: Lista de longitudes de palabras [l1, l2, ..., lk]
            L: Longitud de línea
            b: Amplitud ideal de espacios
        """
        self.palabras = palabras
        self.L = L
        self.b = b
        self.k = len(palabras)
        
    def calcular_costo_linea(self, i: int, j: int) -> float:
        """
        Calcula el costo de poner las palabras desde i hasta j en una línea.
    
        Versión corregida con cálculo consistente.
        """
        # Sumar longitudes de palabras de i a j

        #"casa" "perro" "gato"
        suma_longitudes = sum(self.palabras[i:j+1])
        # 4 + 5 +4 = 13 caracteres
        num_palabras = j - i + 1
        # 3
        num_espacios = num_palabras - 1
        # 3 - 1 = 2 espacios entre palabras
    
        # Verificar si cabe en la línea
        espacio_necesario = suma_longitudes + num_espacios
        # 13 + 2 = 15 caracteres en total
        if espacio_necesario > self.L:
            #Si no cabe, costo infinito
            return float('inf')
    
        # Si es la última línea
        if j == self.k - 1:
            # Última línea: costo bajo pero no cero
            espacio_sobrante = self.L - espacio_necesario
            # Pequeña penalización por espacio sobrante
            return (espacio_sobrante / self.L) ** 2
    
        # Para líneas regulares
        if num_espacios == 0:
            # Una sola palabra
            espacio_sobrante = self.L - suma_longitudes
            # Penalización cuadrática por espacio desperdiciado
            return (espacio_sobrante / self.L) ** 2
        else:
            # Múltiples palabras
            espacio_sobrante = self.L - espacio_necesario
            b_prima = 1.0 + (espacio_sobrante / num_espacios)
            # Espacio real entre palabras (valor que refleja que tan diferente es del ideal)
        
            # Costo principal: desviación del espacio ideal
            costo_espacios = num_espacios * ((b_prima - self.b) ** 2)

        
            # Costo adicional: espacio sobrante no utilizado
            costo_sobrante = (espacio_sobrante / self.L) ** 2
        
            return costo_espacios + costo_sobrante
    
    # ===================== ALGORITMO ITERATIVO (Programación Dinámica) =====================
    def resolver_iterativo(self) -> Tuple[float, List[int]]:
        """
        Algoritmo iterativo usando programación dinámica bottom-up.
        
        Returns:
            (costo_minimo, puntos_de_corte) donde puntos_de_corte son índices 0-based
            de las últimas palabras de cada línea (EXCLUYENDO la última línea)
        """
        n = self.k
        dp = [float('inf')] * (n + 1)
        dp[0] = 0.0
        parent = [-1] * (n + 1)
        
        for i in range(1, n + 1):
            for j in range(i):
                costo_linea = self.calcular_costo_linea(j, i - 1)
                
                if costo_linea == float('inf'):
                    continue
                    
                costo_total = dp[j] + costo_linea
                
                if costo_total < dp[i]:
                    dp[i] = costo_total
                    parent[i] = j
        
        # Reconstruir los cortes
        cortes: List[int] = []
        i = n
        
        while i > 0 and parent[i] != -1:
            # El índice de la última palabra de esta línea es i-1
            # Solo agregar si no es la última palabra del texto
            if i - 1 < n - 1:  # No es la última palabra
                cortes.append(i - 1)
            i = parent[i]
        
        # Los cortes están en orden inverso
        cortes.reverse()
        
        # Eliminar cortes duplicados o en orden incorrecto
        cortes_filtrados = []
        prev = -1
        for corte in cortes:
            if corte > prev:
                cortes_filtrados.append(corte)
                prev = corte
        
        return dp[n], cortes_filtrados
    # ===================== ALGORITMO RECURSIVO PURO =====================
    def resolver_recursivo(self) -> Tuple[float, List[int]]:
        """
        Algoritmo recursivo puro sin memorización.
    
        Returns:
            (costo_minimo, puntos_de_corte) donde puntos_de_corte son índices 0-based
        """
        def recursivo_aux(pos: int) -> Tuple[float, List[int]]:
            """
            Calcula el costo mínimo desde la posición pos hasta el final.
            
            Returns:
                (costo, puntos_de_corte desde pos - índices 0-based)
            """
            if pos == self.k:
                return 0.0, []
            
            mejor_costo = float('inf')
            mejor_corte: List[int] = []
            
            # Probar todas las posibles siguientes líneas
            for siguiente in range(pos + 1, self.k + 1):
                # Línea con palabras desde pos hasta siguiente-1
                costo_linea = self.calcular_costo_linea(pos, siguiente - 1)
                
                if costo_linea < float('inf'):
                    costo_resto, cortes_resto = recursivo_aux(siguiente)
                    costo_total = costo_linea + costo_resto
                    
                    if costo_total < mejor_costo:
                        mejor_costo = costo_total
                        # Los cortes son índices 0-based
                        mejor_corte = [siguiente - 1] + cortes_resto
            
            return mejor_costo, mejor_corte
        
        costo, cortes = recursivo_aux(0)
        # Filtrar el último corte si es el final
        if cortes and cortes[-1] == self.k - 1:
            cortes = cortes[:-1]
        return costo, cortes
    
    # ===================== ALGORITMO DIVIDE Y VENCERÁS =====================
    def resolver_divide_venceras(self) -> Tuple[float, List[int]]:
        """
        Algoritmo usando técnica de divide y vencerás con memorización.
    
        Returns:
            (costo_minimo, puntos_de_corte) donde puntos_de_corte son índices 0-based
        """
        memo: Dict[Tuple[int, int], Tuple[float, List[int]]] = {}
        
        def divide_aux(inicio: int, fin: int) -> Tuple[float, List[int]]:
            """
            Resuelve el subproblema para palabras desde inicio hasta fin.
            """
            if inicio >= fin:
                return 0.0, []
            
            if (inicio, fin) in memo:
                return memo[(inicio, fin)]
            
            mejor_costo = float('inf')
            mejor_corte: List[int] = []
            
            # Dividir el problema
            for punto_division in range(inicio + 1, fin + 1):
                # Primera parte: [inicio, punto_division)
                costo_linea = self.calcular_costo_linea(inicio, punto_division - 1)
                
                if costo_linea < float('inf'):
                    # Segunda parte: [punto_division, fin)
                    costo_resto, cortes_resto = divide_aux(punto_division, fin)
                    costo_total = costo_linea + costo_resto
                    
                    if costo_total < mejor_costo:
                        mejor_costo = costo_total
                        # Los cortes son índices 0-based
                        mejor_corte = [punto_division - 1] + cortes_resto
            
            memo[(inicio, fin)] = (mejor_costo, mejor_corte)
            return mejor_costo, mejor_corte
        
        costo, cortes = divide_aux(0, self.k)
        # Filtrar el último corte si es el final
        if cortes and cortes[-1] == self.k - 1:
            cortes = cortes[:-1]
        return costo, cortes
    
    # ===================== ALGORITMO EXHAUSTIVO =====================
    def resolver_exhaustivo(self) -> Tuple[float, List[int]]:
        """
        Algoritmo exhaustivo que prueba todas las combinaciones posibles.
    
        Returns:
            (costo_minimo, puntos_de_corte) donde puntos_de_corte son índices 0-based
        """
        def generar_particiones(n: int) -> List[List[int]]:
            """Genera todas las particiones posibles de n elementos"""
            if n == 0:
                return [[]]
            
            particiones: List[List[int]] = []
            for i in range(1, n + 1):
                for resto in generar_particiones(n - i):
                    particiones.append([i] + resto)
            
            return particiones
        
        mejor_costo = float('inf')
        mejor_particion: List[int] = []
        
        # Generar todas las particiones posibles
        for particion in generar_particiones(self.k):
            costo_total = 0.0
            pos = 0
            valida = True
            
            # Calcular costo de esta partición
            for tamaño in particion:
                costo_linea = self.calcular_costo_linea(pos, pos + tamaño - 1)
                if costo_linea == float('inf'):
                    valida = False
                    break
                costo_total += costo_linea
                pos += tamaño
            
            if valida and costo_total < mejor_costo:
                mejor_costo = costo_total
                mejor_particion = particion
        
        # Convertir partición a puntos de corte (0-based)
        puntos_corte: List[int] = []
        acum = 0
        for tamaño in mejor_particion:
            acum += tamaño
            if acum < self.k:  # No incluir el final
                puntos_corte.append(acum - 1)  # Convertir a 0-based
        
        return mejor_costo, puntos_corte


def ejecutar_y_medir(algoritmo_func, nombre: str, umbral_lento: float = TIEMPO_UMBRAL_LENTO) -> Dict:
    """
    Ejecuta un algoritmo y mide su rendimiento.
    
    Returns:
        Diccionario con resultados y métricas
    """
    print(f"\nEjecutando {nombre}...")
    inicio = time.perf_counter()
    try:
        costo, cortes = algoritmo_func()
        tiempo = time.perf_counter() - inicio

        if tiempo > umbral_lento:
            print(
                f"Aviso: {nombre} está tardando más de lo normal "
                f"({tiempo:.3f} s). Esto es esperable para algoritmos de "
                f"alta complejidad (por ejemplo, recursivo puro o exhaustivo)."
            )

        return {
            'nombre': nombre,
            'costo': costo,
            'cortes': cortes,
            'tiempo': tiempo,
            'exito': True,
            'error': None
        }
    except Exception as e:
        tiempo = time.perf_counter() - inicio
        print(f"❌ Error ejecutando {nombre}: {e}")
        return {
            'nombre': nombre,
            'costo': None,
            'cortes': None,
            'tiempo': tiempo,
            'exito': False,
            'error': str(e)
        }


def mostrar_solucion(palabras: List[int], cortes: List[int], L: int, b: float):
    """Muestra la solución de manera legible"""
    print("\nDistribución de palabras en líneas:")
    print("=" * 60)
    
    # Si no hay cortes, toda la entrada está en una línea
    if not cortes:
        suma = sum(palabras)
        num_espacios = len(palabras) - 1
        espacio_total = suma + num_espacios
        
        if num_espacios > 0:
            b_prima = (L - suma) / num_espacios
        else:
            b_prima = 0
        
        print(f"Línea 1: palabras 1 a {len(palabras)}")
        print(f"  Longitudes: {palabras}")
        print(f"  Suma longitudes: {suma}")
        print(f"  Espacios totales: {espacio_total}/{L}")
        print(f"  Espacios reales: {b_prima:.2f} (ideal: {b})")
        print()
        return
    
    inicio = 0
    linea_num = 1
    
    # Mostrar líneas definidas por cortes
    for corte in cortes:
        # corte es el índice de la última palabra de esta línea
        fin = corte + 1
        
        if inicio >= fin:
            continue
            
        linea = palabras[inicio:fin]
        suma = sum(linea)
        num_espacios = len(linea) - 1
        espacio_total = suma + num_espacios
        
        if num_espacios > 0:
            b_prima = (L - suma) / num_espacios
        else:
            b_prima = 0
        
        print(f"Línea {linea_num}: palabras {inicio+1} a {fin}")
        print(f"  Longitudes: {linea}")
        print(f"  Suma longitudes: {suma}")
        print(f"  Espacios totales: {espacio_total}/{L}")
        print(f"  Espacios reales: {b_prima:.2f} (ideal: {b})")
        print()
        
        inicio = fin
        linea_num += 1
    
    # Mostrar última línea
    if inicio < len(palabras):
        linea = palabras[inicio:]
        suma = sum(linea)
        num_espacios = len(linea) - 1
        espacio_total = suma + num_espacios
        
        if num_espacios > 0:
            b_prima = (L - suma) / num_espacios
        else:
            b_prima = 0
        
        print(f"Línea {linea_num}: palabras {inicio+1} a {len(palabras)}")
        print(f"  Longitudes: {linea}")
        print(f"  Suma longitudes: {suma}")
        print(f"  Espacios totales: {espacio_total}/{L}")
        print(f"  Espacios reales: {b_prima:.2f} (ideal: {b})")
        print()

def ejecutar_comparacion():
    """Función principal para ejecutar y comparar todos los algoritmos"""
    
    print("=" * 70)
    print("PROYECTO: DIVISIÓN EN PÁRRAFOS")
    print("Análisis y Diseño de Algoritmos")
    print("=" * 70)
    
    # Ejemplo 1: Pequeño (para probar todos los algoritmos)
    print("\n\nCASO DE PRUEBA 1: Entrada pequeña")
    print("-" * 70)
    palabras1 = [5, 3, 4, 6, 2]
    L1 = 15
    b1 = 1.5
    
    print(f"Palabras (longitudes): {palabras1}")
    print(f"Longitud de línea (L): {L1}")
    print(f"Amplitud ideal de espacios (b): {b1}")
    
    dp1 = DivisionParrafos(palabras1, L1, b1)
    
    resultados1: List[Dict] = []
    resultados1.append(ejecutar_y_medir(dp1.resolver_iterativo, "Iterativo (DP)"))
    resultados1.append(ejecutar_y_medir(dp1.resolver_recursivo, "Recursivo Puro"))
    resultados1.append(ejecutar_y_medir(dp1.resolver_divide_venceras, "Divide y Vencerás"))
    resultados1.append(ejecutar_y_medir(dp1.resolver_exhaustivo, "Exhaustivo"))
    
    print("\nRESULTADOS:")
    print("-" * 70)
    for res in resultados1:
        if res['exito']:
            print(f"{res['nombre']:25} | Costo: {res['costo']:10.4f} | Tiempo: {res['tiempo']*1000:10.4f} ms")
        else:
            print(f"{res['nombre']:25} | ERROR: {res['error']}")
    
    # Mostrar solución óptima (menor costo entre los que terminaron bien)
    sol_optima1 = min(
        (r for r in resultados1 if r['exito']),
        key=lambda r: r['costo']
    )
    print(f"\n✅ Mejor solución (CASO 1): {sol_optima1['nombre']} con costo {sol_optima1['costo']:.4f}")
    mostrar_solucion(palabras1, sol_optima1['cortes'], L1, b1)
    
    # Ejemplo 2: Mediano (también ejecuta todos los algoritmos)
    print("\n\nCASO DE PRUEBA 2: Entrada mediana")
    print("-" * 70)
    palabras2 = [3, 4, 2, 5, 3, 4, 6, 2, 3, 5]
    L2 = 20
    b2 = 2.0
    
    print(f"Palabras (longitudes): {palabras2}")
    print(f"Longitud de línea (L): {L2}")
    print(f"Amplitud ideal de espacios (b): {b2}")
    
    dp2 = DivisionParrafos(palabras2, L2, b2)
    
    resultados2: List[Dict] = []
    resultados2.append(ejecutar_y_medir(dp2.resolver_iterativo, "Iterativo (DP)"))
    resultados2.append(ejecutar_y_medir(dp2.resolver_recursivo, "Recursivo Puro"))
    resultados2.append(ejecutar_y_medir(dp2.resolver_divide_venceras, "Divide y Vencerás"))
    resultados2.append(ejecutar_y_medir(dp2.resolver_exhaustivo, "Exhaustivo"))
    
    print("\nRESULTADOS:")
    print("-" * 70)
    for res in resultados2:
        if res['exito']:
            print(f"{res['nombre']:25} | Costo: {res['costo']:10.4f} | Tiempo: {res['tiempo']*1000:10.4f} ms")
        else:
            print(f"{res['nombre']:25} | ERROR: {res['error']}")
    
    sol_optima2 = min(
        (r for r in resultados2 if r['exito']),
        key=lambda r: r['costo']
    )
    print(f"\n✅ Mejor solución (CASO 2): {sol_optima2['nombre']} con costo {sol_optima2['costo']:.4f}")
    mostrar_solucion(palabras2, sol_optima2['cortes'], L2, b2)
    
    print("\n\nANÁLISIS DE COMPLEJIDAD TEMPORAL")
    print("=" * 100)
    print(f"{'Algoritmo':<25} | {'Por Valor (n)':<20} | {'Por Bits (b=log₂n)':<25} | {'Descripción'}")
    print("-" * 100)
    print(f"{'Iterativo (DP)':<25} | {'O(n²)':<20} | {'O(2^(2b))':<25} | Pseudo-polinomial")
    print(f"{'Recursivo Puro':<25} | {'O(2ⁿ)':<20} | {'O(2^(2^b))':<25} | Exponencial sin memo")
    print(f"{'Divide y Vencerás':<25} | {'O(n²)':<20} | {'O(2^(2b))':<25} | Pseudo-polinomial")
    print(f"{'Exhaustivo':<25} | {'O(B(n))':<20} | {'O(B(2^b))':<25} | Súper-exponencial")

    print("\n\n✅ CONCLUSIÓN:")
    print("-" * 70)
    print("El algoritmo ITERATIVO (Programación Dinámica) es el más eficiente")
    print("para este problema, con complejidad O(n²) y uso de memoria O(n).")


if __name__ == "__main__":
    ejecutar_comparacion()