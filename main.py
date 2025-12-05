"""
Script Principal Integrado - División en Párrafos
Ejecuta todas las funcionalidades del proyecto en un solo comando
"""

import sys
#Controla la salida del programa y obtiene rutas del intérprete Python
import os
#Permite ejecutar comandos del sistema operativo
import subprocess
#Ejecuta comandos externos como pytest
from typing import Optional
#Define tipos de datos opcionales para mejor documentación
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
            '8': ('Stress test con entradas grandes', self.ejecutar_casos_grandes),
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
        #Núcleo del proyecto - Implementa los 4 algoritmos
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
                print(f"\nLongitudes: {palabras}")
            
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
        
        # Reconstruir todas las líneas para análisis
        lineas = []
        if not cortes:
            lineas.append(palabras_texto)
        else:
            inicio = 0
            for corte in cortes:
                fin = corte + 1
                if inicio < fin:
                    lineas.append(palabras_texto[inicio:fin])
                    inicio = fin
            
            if inicio < len(palabras_texto):
                lineas.append(palabras_texto[inicio:])
        
        # Mostrar solución formateada
        for i, linea in enumerate(lineas, 1):
            linea_str = " ".join(linea)
            # Mostrar línea con número
            print(f"Línea {i:2}: {linea_str}")
        
        print("=" * 80)
        
        # Análisis de la solución
        print("\nANÁLISIS DE LA SOLUCIÓN:")
        print("-" * 80)
        
        # Usar variable para b' para evitar problema de backslash
        b_prime_header = "b'"
        print(f"{'Línea':<6} {'Palabras':<25} {'Uso':<10} {b_prime_header:<8} {'Costo':<10} {'Decisión'}")
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
                
            # Calcular costo REAL
            costo_linea = dp.calcular_costo_linea(inicio, fin - 1)
            
            linea_palabras = palabras_texto[inicio:fin]
            linea_longitudes = longitudes[inicio:fin]
            
            suma = sum(linea_longitudes)
            num_palabras = len(linea_longitudes)
            num_espacios = num_palabras - 1
            espacio_total = suma + num_espacios
            uso_porcentaje = (espacio_total / L) * 100 if L > 0 else 0
            
            if num_espacios > 0:
                b_prima = (L - suma) / num_espacios
                b_prima_str = f"{b_prima:.2f}"
            else:
                b_prima_str = "N/A"
            
            # Determinar tipo de decisión
            if num_palabras == 1:
                decision = "Palabra sola"
            elif fin == len(palabras_texto):
                decision = "Última línea"
            elif abs(b_prima - b) < 0.1:
                decision = "Agrupamiento perfecto"
            elif abs(b_prima - b) < 2.0:
                decision = "Agrupamiento aceptable"
            else:
                decision = "Agrupamiento costoso"
            
            # Formatear uso
            uso_str = f"{espacio_total:2d}/{L} ({uso_porcentaje:3.0f}%)"
            
            print(f"{linea_num:<6} {' '.join(linea_palabras):<25} "
                f"{uso_str:<10} {b_prima_str:<8} {costo_linea:<10.4f} {decision}")
            
            if costo_linea != float('inf'):
                costo_total_calculado += costo_linea
            
            inicio = fin
            linea_num += 1
        
        print("-" * 80)
        costo_optimo = dp.resolver_iterativo()[0]
        print(f"RESUMEN:")
        print(f"   • Total de líneas: {len(lineas)}")
        print(f"   • Costo total calculado: {costo_total_calculado:.4f}")
        print(f"   • Costo óptimo reportado: {costo_optimo:.4f}")
        print(f"   • Eficiencia promedio: {sum(longitudes) / (len(lineas) * L) * 100:.1f}%")
        
        if abs(costo_total_calculado - costo_optimo) > 0.001:
            print("   ADVERTENCIA: Los costos no coinciden. Puede haber error en la reconstrucción.")
        
        print("-" * 80)
        
        # Explicación de decisiones clave
        print("\nEXPLICACIÓN DE DECISIONES:")
        print("-" * 80)
        
        # Analizar decisiones interesantes
        inicio = 0
        for i, fin in enumerate(fines_linea):
            if inicio >= fin:
                continue
                
            linea_palabras = palabras_texto[inicio:fin]
            linea_longitudes = longitudes[inicio:fin]
            num_palabras = len(linea_palabras)
            
            if num_palabras > 1:
                suma = sum(linea_longitudes)
                num_espacios = num_palabras - 1
                b_prima = (L - suma) / num_espacios
                
                if abs(b_prima - b) > 2.0:
                    print(f"• {' '.join(linea_palabras)}: b'={b_prima:.2f} (muy diferente de b={b})")
                    print(f"  → Espacios desiguales hacen costoso agrupar")
                elif fin == len(palabras_texto):
                    print(f"• {' '.join(linea_palabras)}: Última línea con costo reducido")
                    print(f"  → El algoritmo permite más flexibilidad al final")
                elif abs(b_prima - b) < 0.1:
                    print(f"• {' '.join(linea_palabras)}: Agrupamiento perfecto (b'={b_prima:.2f})")
                    print(f"  → Espacios ideales, costo mínimo")
            
            inicio = fin
        
        # Representación interna
        print("\nREPRESENTACIÓN INTERNA (solo longitudes):")
        print("=" * 60)
        
        from division_parrafos import mostrar_solucion
        mostrar_solucion(longitudes, cortes, L, b)

    def _mostrar_solucion_solo_longitudes(self, longitudes, cortes, L, b):
        """Muestra la solución cuando el usuario ingresó solo longitudes"""
        print("\n" + "=" * 80)
        print("SOLUCIÓN (representación con longitudes):")
        print("=" * 80)
        
        from division_parrafos import mostrar_solucion
        mostrar_solucion(longitudes, cortes, L, b)

    def ejecutar_casos_grandes(self):
        """
        Ejecuta ejemplos con entradas muy grandes para testear el comportamiento
        de las implementaciones (stress test) y genera gráficas de n vs tiempo.
        """
        print("\nSTRESS TEST CON ENTRADAS GRANDES")
        print("=" * 80)

        from division_parrafos import DivisionParrafos, ejecutar_y_medir
        from analisis_graficas import AnalizadorRendimiento
        import random

        # Tamaños grandes: de 500 en 500 hasta 3500
        tamanos = list(range(500, 3501, 500))  # [500, 1000, ..., 5000]
        L = 60    # longitud de línea fija para las pruebas
        b = 1.5   # amplitud ideal de espacios

        resultados_stress = []

        for n in tamanos:
            print(f"\nInstancia con n = {n} palabras")
            print("-" * 80)
            # Longitudes aleatorias de palabras entre 2 y 10 caracteres
            palabras = [random.randint(2, 10) for _ in range(n)]
            print(f"Primeras 10 longitudes: {palabras[:10]} ...")
            print(f"L = {L}, b = {b}")

            dp = DivisionParrafos(palabras, L, b)

            resultados_alg = []
            resultado_n = {
                'n': n,
                'algoritmos': {}
            }

            # Iterativo
            res_iter = ejecutar_y_medir(dp.resolver_iterativo, f"Iterativo (DP)      n={n}")
            resultados_alg.append(res_iter)
            if res_iter['exito'] and res_iter['costo'] is not None:
                resultado_n['algoritmos']['Iterativo'] = {
                    'tiempo': res_iter['tiempo'],
                    'costo': res_iter['costo']
                }

            # Divide y Vencerás
            res_dyv = ejecutar_y_medir(dp.resolver_divide_venceras, f"Divide y Vencerás  n={n}")
            resultados_alg.append(res_dyv)
            if res_dyv['exito'] and res_dyv['costo'] is not None:
                resultado_n['algoritmos']['Divide y Vencerás'] = {
                    'tiempo': res_dyv['tiempo'],
                    'costo': res_dyv['costo']
                }

            # Opcional: también recursivo y exhaustivo si el usuario quiere
            resp = input(
                "\n¿Intentar también Recursivo Puro y Exhaustivo para este tamaño? "
                "(puede tardar MUCHÍSIMO o no terminar) [s/N]: "
            ).strip().lower()

            if resp == "s":
                res_rec = ejecutar_y_medir(dp.resolver_recursivo, f"Recursivo Puro      n={n}")
                resultados_alg.append(res_rec)
                if res_rec['exito'] and res_rec['costo'] is not None:
                    resultado_n['algoritmos']['Recursivo'] = {
                        'tiempo': res_rec['tiempo'],
                        'costo': res_rec['costo']
                    }

                res_exh = ejecutar_y_medir(dp.resolver_exhaustivo, f"Exhaustivo          n={n}")
                resultados_alg.append(res_exh)
                if res_exh['exito'] and res_exh['costo'] is not None:
                    resultado_n['algoritmos']['Exhaustivo'] = {
                        'tiempo': res_exh['tiempo'],
                        'costo': res_exh['costo']
                    }

            print("\nResumen de resultados (n = {}):".format(n))
            print("-" * 80)
            for res in resultados_alg:
                if res["exito"]:
                    costo_str = f"{res['costo']:.4f}" if res["costo"] is not None else "N/A"
                    print(
                        f"{res['nombre']:30} | "
                        f"Costo: {costo_str:>10} | "
                        f"Tiempo: {res['tiempo']*1000:10.4f} ms"
                    )
                else:
                    print(f"{res['nombre']:30} | ERROR: {res['error']}")

            resultados_stress.append(resultado_n)

        print("\nStress test finalizado.")

        # ----- Generar gráficas y tabla para estos resultados grandes -----
        print("\nGenerando análisis y gráficas del stress test (n grandes)...")
        analizador = AnalizadorRendimiento()
        analizador.resultados = resultados_stress

        # Tabla comparativa y JSON específico del stress test
        analizador.generar_tabla_comparativa()
        analizador.guardar_resultados_json('resultados_benchmark_stress.json')

        # Gráficas específicas del stress test
        analizador.generar_graficas(
            guardar=True,
            filename='analisis_division_parrafos_stress.png'
        )

        self.pausar()
    
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