"""
Script Principal Integrado - División en Párrafos
Ejecuta todas las funcionalidades del proyecto en un solo comando
"""

import sys
import os
import subprocess
from typing import Optional
import time

class MenuPrincipal:
    """Menú interactivo para el proyecto"""
    
    def __init__(self):
        self.opciones = {
            '1': ('Ejecutar algoritmos con casos de prueba', self.ejecutar_casos_prueba),
            '2': ('Ejecutar análisis de rendimiento y gráficas', self.ejecutar_analisis),
            '3': ('Ejecutar tests con pytest', self.ejecutar_tests),
            '4': ('Ejecutar tests con cobertura', self.ejecutar_tests_cobertura),
            '5': ('Ver documentación del proyecto', self.ver_documentacion),
            '6': ('Ejecutar TODO (casos + análisis + tests)', self.ejecutar_todo),
            '7': ('Ejemplo personalizado', self.ejemplo_personalizado),
            '0': ('Salir', None)
        }
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        print("\n" + "=" * 80)
        print("PROYECTO: DIVISIÓN EN PÁRRAFOS")
        print("Análisis y Diseño de Algoritmos")
        print("=" * 80)
        print("\nSelecciona una opción:\n")
        
        for key, (descripcion, _) in sorted(self.opciones.items()):
            print(f"  [{key}] {descripcion}")
        
        print("\n" + "-" * 80)
    
    def ejecutar_casos_prueba(self):
        """Ejecuta los casos de prueba predefinidos"""
        print("\nEjecutando casos de prueba...")
        print("-" * 80)
        
        from division_parrafos import ejecutar_comparacion
        ejecutar_comparacion()
        
        self.pausar()
    
    def ejecutar_analisis(self):
        """Ejecuta el análisis completo con gráficas"""
        print("\nEjecutando análisis de rendimiento...")
        print("-" * 80)
        
        from analisis_graficas import main as analisis_main
        analisis_main()
        
        self.pausar()
    
    def ejecutar_tests(self):
        """Ejecuta los tests con pytest"""
        print("\nEjecutando tests con pytest...")
        print("-" * 80)
        
        try:
            # Importar pytest directamente
            import pytest
            
            # Ejecutar pytest programáticamente
            print("\nEjecutando: pytest test_division_parrafos.py -v --tb=short\n")
            resultado = pytest.main([
                'test_division_parrafos.py',
                '-v',
                '--tb=short'
            ])
            
            if resultado == 0:
                print("\n✅ Todos los tests pasaron correctamente")
            else:
                print("\nAlgunos tests fallaron o fueron omitidos")
                
        except ImportError:
            print("\n❌ pytest no está instalado.")
            print("\nInstala pytest con:")
            print("   pip install pytest")
            print("\nO ejecuta los tests manualmente:")
            print("   python -m pytest test_division_parrafos.py -v")
        except Exception as e:
            print(f"\n❌ Error al ejecutar pytest: {e}")
            print("\nIntenta ejecutar manualmente desde la terminal:")
            print("   python -m pytest test_division_parrafos.py -v")
        
        self.pausar()
    
    def ejecutar_tests_cobertura(self):
        """Ejecuta tests con reporte de cobertura"""
        print("\nEjecutando tests con cobertura...")
        print("-" * 80)
        
        try:
            # Verificar si pytest-cov está instalado
            import pytest_cov
            import pytest
            
            # Ejecutar con cobertura
            print("\nEjecutando: pytest test_division_parrafos.py -v --cov=division_parrafos\n")
            resultado = pytest.main([
                'test_division_parrafos.py',
                '-v',
                '--cov=division_parrafos',
                '--cov-report=term-missing'
            ])
            
            if resultado == 0:
                print("\n✅ Tests completados. Ver reporte de cobertura arriba.")
            
        except ImportError as e:
            if 'pytest_cov' in str(e):
                print("\npytest-cov no está instalado.")
                print("Instala con: pip install pytest-cov")
                print("\nEjecutando tests normales sin cobertura...")
                self.ejecutar_tests()
                return
            else:
                print("\n❌ pytest no está instalado.")
                print("Instala con: pip install pytest pytest-cov")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nIntenta ejecutar manualmente desde la terminal:")
            print("   python -m pytest test_division_parrafos.py --cov=division_parrafos")
        
        self.pausar()

    def ver_documentacion(self):
        """Muestra información del proyecto"""
        print("\nDOCUMENTACIÓN DEL PROYECTO")
        print("=" * 80)
        
        print("""
Este proyecto implementa 4 algoritmos para el problema de División en Párrafos:

1. ITERATIVO (Programación Dinámica) - O(n²)
   Más eficiente, recomendado para producción
   
2. RECURSIVO PURO - O(2ⁿ)
   Exponencial, solo para demostración (n ≤ 10)
   
3. DIVIDE Y VENCERÁS - O(n²)
   ✅ Alternativa válida con memoización
   
4. EXHAUSTIVO - O(B(n))
   ❌ Extremadamente lento, solo n ≤ 5

ARCHIVOS PRINCIPALES:
- division_parrafos.py       : Implementación de algoritmos
- test_division_parrafos.py  : Suite de pruebas (pytest)
- analisis_graficas.py       : Análisis y visualización
- main.py                    : Este menú interactivo

RESULTADOS GENERADOS:
- analisis_division_parrafos.png  : Gráficas comparativas
- resultados_benchmark.json       : Datos en JSON

Para más información, consulta README.md
        """)
        
        self.pausar()
    
    def ejecutar_todo(self):
        """Ejecuta todas las funcionalidades"""
        print("\nEJECUCIÓN COMPLETA DEL PROYECTO")
        print("=" * 80)
        
        print("\n1CASOS DE PRUEBA")
        print("-" * 80)
        self.ejecutar_casos_prueba()
        
        print("\n\nANÁLISIS Y GRÁFICAS")
        print("-" * 80)
        self.ejecutar_analisis()
        
        print("\n\nTESTS UNITARIOS")
        print("-" * 80)
        self.ejecutar_tests()
        
        print("\n" + "=" * 80)
        print("✅ EJECUCIÓN COMPLETA FINALIZADA")
        print("=" * 80)
        
        self.pausar()
    
    def ejemplo_personalizado(self):
        """Permite al usuario ingresar sus propios datos"""
        print("\nEJEMPLO PERSONALIZADO")
        print("-" * 80)
    
        try:
            # Solicitar tipo de entrada
            print("\n¿Cómo deseas ingresar las palabras?")
            print("  [1] Palabras reales (texto)")
            print("  [2] Longitudes numéricas")
            opcion = input("Opción (1 o 2): ").strip()
        
            palabras_texto = None
        
            if opcion == "1":
                print("\nIngresa las palabras separadas por espacios:")
                print("Ejemplo: el rápido zorro marrón salta sobre el perro perezoso")
                entrada = input("Palabras: ").strip()
                if not entrada:
                    print("❌ Debes ingresar al menos una palabra")
                    self.pausar()
                    return
                
                palabras_texto = entrada.split()
            
                # Calcular longitudes
                palabras = [len(p) for p in palabras_texto]
            
                print(f"\nPalabras ingresadas: {palabras_texto}")
                print(f"Longitudes calculadas: {palabras}")
            
                # Calcular sugerencia realista para L
                max_longitud = max(palabras)
                avg_longitud = sum(palabras) / len(palabras)
                # Sugerir L basado en: 2-3 palabras promedio + espacios
                sugerencia_L = min(max(20, int(avg_longitud * 3 + 5)), max_longitud * 4)
            
            elif opcion == "2":
                print("\nIngresa las longitudes de las palabras separadas por espacios:")
                print("Ejemplo: 5 3 4 6 2 4 5 3")
                palabras_str = input("Longitudes: ").strip()
                if not palabras_str:
                    print("❌ Debes ingresar al menos una longitud")
                    self.pausar()
                    return
                
                palabras = [int(x) for x in palabras_str.split()]
                print(f"\n📏 Longitudes: {palabras}")
            
                # Calcular sugerencia
                max_longitud = max(palabras)
                avg_longitud = sum(palabras) / len(palabras)
                sugerencia_L = min(max(15, int(avg_longitud * 3 + 5)), max_longitud * 4)
            
            else:
                print("❌ Opción inválida")
                self.pausar()
                return
        
            print(f"\nTen en cuenta que L es la longitud máxima de la línea en caracteres.")
            print(f"Sugerencia: Para estas palabras, prueba con L entre {sugerencia_L-5} y {sugerencia_L+5}")
        
            L_input = input(f"Longitud de línea (L) [sugerido {sugerencia_L}]: ")
            L = int(L_input) if L_input.strip() else sugerencia_L
        
            b_input = input("Amplitud ideal de espacios (b, típicamente 1.0): ")
            b = float(b_input) if b_input.strip() else 1.0
        
            print(f"\nResolviendo con tus parámetros...")
            print(f"L = {L}, b = {b}")
        
            from division_parrafos import DivisionParrafos
            import time
        
            dp = DivisionParrafos(palabras, L, b)
        
            # DEBUG: Mostrar algunos costos de ejemplo
            print(f"\nDEBUG - Costos de ejemplo:")
            print("-" * 50)
            n = len(palabras)
        
            if n >= 1:
                # Costo de primera palabra sola
                costo1 = dp.calcular_costo_linea(0, 0)
                if palabras_texto:
                    palabras_str = ' '.join(palabras_texto[0:1])
                    print(f"Costo '{palabras_str}' solo: {costo1:.4f}")
                else:
                    print(f"Costo palabra {palabras[0]} solo: {costo1:.4f}")
            
                # Costo de primeras 2 palabras juntas
                if n >= 2:
                    costo2 = dp.calcular_costo_linea(0, 1)
                    if palabras_texto:
                        palabras_str = ' '.join(palabras_texto[0:2])
                        print(f"Costo '{palabras_str}' juntas: {costo2:.4f}")
                    else:
                        print(f"Costo palabras {palabras[0]} y {palabras[1]} juntas: {costo2:.4f}")
            
                # Costo de primeras 3 palabras juntas
                if n >= 3:
                    costo3 = dp.calcular_costo_linea(0, 2)
                    if palabras_texto:
                        palabras_str = ' '.join(palabras_texto[0:3])
                        print(f"Costo '{palabras_str}' juntas: {costo3:.4f}")
                    else:
                        print(f"Costo primeras 3 palabras juntas: {costo3:.4f}")
        
            print("-" * 50)
        
            # Resolver con iterativo
            inicio = time.perf_counter()
            costo, cortes = dp.resolver_iterativo()
            tiempo = time.perf_counter() - inicio
        
            print(f"\n✅ SOLUCIÓN ENCONTRADA")
            print(f"Costo óptimo total: {costo:.4f}")
            print(f"Tiempo: {tiempo*1000:.4f} ms")
        
            # Mostrar interpretación de cortes
            print(f"\nInterpretación de cortes (0-based): {cortes}")
            if cortes:
                print("Esto significa que las líneas terminan en las palabras con índices:")
                for i, corte in enumerate(cortes):
                    print(f"  Línea {i+1}: termina en palabra {corte+1} (índice {corte})")
        
            # Mostrar solución
            if palabras_texto:
                self._mostrar_solucion_con_palabras(palabras_texto, palabras, cortes, L, b)
            else:
                self._mostrar_solucion_solo_longitudes(palabras, cortes, L, b)
            
        except ValueError as e:
            print(f"\n❌ Error en la entrada: {e}")
            print("Asegúrate de ingresar números válidos.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
        self.pausar()

    def _mostrar_solucion_con_palabras(self, palabras_texto, longitudes, cortes, L, b):
        """Muestra la solución cuando el usuario ingresó palabras reales"""
        print("\n" + "=" * 80)
        print("PÁRRAFOS FORMATEADOS (con tus palabras):")
        print("=" * 80)
        
        # Crear objeto DivisionParrafos para cálculos consistentes
        from division_parrafos import DivisionParrafos
        dp = DivisionParrafos(longitudes, L, b)
        
        # Mostrar solución
        if not cortes:
            print(" ".join(palabras_texto))
        else:
            inicio = 0
            for corte in cortes:
                fin = corte + 1
                if inicio >= fin:
                    continue
                linea = palabras_texto[inicio:fin]
                print(" ".join(linea))
                inicio = fin
            
            if inicio < len(palabras_texto):
                linea = palabras_texto[inicio:]
                print(" ".join(linea))
        
        print("=" * 80)
        
        # Detalle por línea
        print("\nDETALLE POR LÍNEA:")
        print("-" * 80)
        
        inicio = 0
        costo_total_calculado = 0.0
        linea_num = 1
        
        # Determinar todos los puntos de fin
        if cortes:
            fines_linea = [c + 1 for c in cortes]
            if fines_linea[-1] < len(palabras_texto):
                fines_linea.append(len(palabras_texto))
        else:
            fines_linea = [len(palabras_texto)]
        
        for fin in fines_linea:
            if inicio >= fin:
                continue
                
            # Calcular costo REAL usando la misma función
            costo_linea = dp.calcular_costo_linea(inicio, fin - 1)
            
            linea_palabras = palabras_texto[inicio:fin]
            linea_longitudes = longitudes[inicio:fin]
            
            suma = sum(linea_longitudes)
            num_palabras = len(linea_longitudes)
            num_espacios = num_palabras - 1
            espacio_total = suma + num_espacios
            
            print(f"\nLínea {linea_num}:")
            print(f"  Palabras           : {' '.join(linea_palabras)}")
            print(f"  Índices (1-based)  : {inicio+1} a {fin}")
            print(f"  Número de palabras : {num_palabras}")
            print(f"  Longitud palabras  : {suma} caracteres")
            print(f"  Espacios necesarios: {espacio_total}/{L}")
            
            if num_espacios > 0:
                b_prima = (L - suma) / num_espacios
                print(f"  b' calculado       : {b_prima:.4f}")
            
            if fin == len(palabras_texto):
                print(f"  Costo de la línea  : {costo_linea:.4f} (última línea)")
            else:
                print(f"  Costo de la línea  : {costo_linea:.4f}")
            
            if costo_linea != float('inf'):
                costo_total_calculado += costo_linea
            
            inicio = fin
            linea_num += 1
        
        print("\n" + "-" * 80)
        print(f"COSTO TOTAL CALCULADO: {costo_total_calculado:.4f}")
        print(f"COSTO ÓPTIMO REPORTADO: {dp.resolver_iterativo()[0]:.4f}")
        print("-" * 80)
        
        # Verificar consistencia
        if abs(costo_total_calculado - dp.resolver_iterativo()[0]) > 0.001:
            print("ADVERTENCIA: Los costos no coinciden. Puede haber error en la reconstrucción.")
        
        # Representación interna
        print("\n🔢 REPRESENTACIÓN INTERNA (solo longitudes):")
        from division_parrafos import mostrar_solucion
        mostrar_solucion(longitudes, cortes, L, b)


    def _mostrar_solucion_solo_longitudes(self, longitudes, cortes, L, b):
        """Muestra la solución cuando el usuario ingresó solo longitudes"""
        print("\n" + "=" * 80)
        print("SOLUCIÓN (representación con longitudes):")
        print("=" * 80)
        
        from division_parrafos import mostrar_solucion
        mostrar_solucion(longitudes, cortes, L, b)
    
    def pausar(self):
        """Pausa la ejecución esperando input del usuario"""
        input("\nPresiona ENTER para continuar...")
    
    def ejecutar(self):
        """Ejecuta el menú principal"""
        while True:
            self.mostrar_menu()
            
            opcion = input("\nOpción: ").strip()
            
            if opcion == '0':
                print("\n¡Hasta luego!")
                sys.exit(0)
            
            if opcion in self.opciones:
                _, funcion = self.opciones[opcion]
                if funcion:
                    try:
                        funcion()
                    except KeyboardInterrupt:
                        print("\n\nOperación cancelada por el usuario")
                        self.pausar()
                    except Exception as e:
                        print(f"\n❌ Error: {e}")
                        import traceback
                        traceback.print_exc()
                        self.pausar()
            else:
                print("\n❌ Opción inválida. Intenta de nuevo.")
                self.pausar()


def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    dependencias = {
        'pytest': 'pytest',
        'matplotlib': 'matplotlib',
        'numpy': 'numpy'
    }
    
    faltantes = []
    
    for modulo, nombre_pip in dependencias.items():
        try:
            __import__(modulo)
        except ImportError:
            faltantes.append(nombre_pip)
    
    if faltantes:
        print("\nADVERTENCIA: Faltan dependencias")
        print("-" * 80)
        print("\nInstala las dependencias faltantes con:")
        print(f"pip install {' '.join(faltantes)}")
        print("\nO instala todas con:")
        print("pip install -r requirements.txt")
        print("-" * 80)
        
        respuesta = input("\n¿Deseas continuar de todas formas? (s/n): ").strip().lower()
        if respuesta != 's':
            sys.exit(1)


def main():
    """Función principal"""
    # Verificar dependencias
    verificar_dependencias()
    
    # Ejecutar menú
    menu = MenuPrincipal()
    
    try:
        menu.ejecutar()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido.")
        sys.exit(0)


if __name__ == "__main__":
    main()