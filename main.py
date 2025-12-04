"""
Script Principal Integrado - División en Párrafos
Ejecuta todas las funcionalidades del proyecto en un solo comando
"""

import sys
import os
import subprocess
from typing import Optional


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
        
        resultado = subprocess.run(
            [
                sys.executable,
                "-m", "pytest",
                "test_division_parrafos.py",
                "-v",
                "--tb=short",
            ],
            capture_output=False
        )
        
        if resultado.returncode == 0:
            print("\n✅ Todos los tests pasaron correctamente")
        else:
            print("\n❌ Algunos tests fallaron")
        
        self.pausar()
    
    def ejecutar_tests_cobertura(self):
        """Ejecuta tests con reporte de cobertura"""
        print("\nEjecutando tests con cobertura...")
        print("-" * 80)

        try:
            import pytest
            import pytest_cov  # verificar que el plugin exista
        except ImportError:
            print("\npytest-cov no está instalado.")
            print("Instala con: pip install pytest pytest-cov")
            self.pausar()
            return

        args = [
            "test_division_parrafos.py",
            "-v",
            "--cov=division_parrafos",
            "--cov-report=term-missing",
        ]

        try:
            exit_code = pytest.main(args)
        except SystemExit as e:
            exit_code = e.code

        if exit_code == 0:
            print("\n✅ Tests completados. Ver reporte de cobertura arriba.")
        else:
            print("\n❌ Algunos tests fallaron (ver detalles arriba).")

        self.pausar()
    
    def ver_documentacion(self):
        """Muestra información del proyecto"""
        print("\nDOCUMENTACIÓN DEL PROYECTO")
        print("=" * 80)
        
        print("""
Este proyecto implementa 4 algoritmos para el problema de División en Párrafos:

1. ITERATIVO (Programación Dinámica) - O(n²)
   ✅ Más eficiente, recomendado para producción
   
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
- analisis_division_parrafos.png          : Gráficas comparativas (tamaños pequeños/medios)
- analisis_division_parrafos_stress.png   : Gráficas del stress test (tamaños grandes)
- resultados_benchmark.json               : Datos en JSON (benchmark estándar)
- resultados_benchmark_stress.json        : Datos en JSON (stress test)

Para más información, consulta README.md
        """)
        
        self.pausar()
    
    def ejecutar_todo(self):
        """Ejecuta todas las funcionalidades"""
        print("\nEJECUCIÓN COMPLETA DEL PROYECTO")
        print("=" * 80)
        
        print("\n1️  CASOS DE PRUEBA")
        print("-" * 80)
        self.ejecutar_casos_prueba()
        
        print("\n\n2️  ANÁLISIS Y GRÁFICAS")
        print("-" * 80)
        self.ejecutar_analisis()
        
        print("\n\n3️  TESTS UNITARIOS")
        print("-" * 80)
        self.ejecutar_tests()
        
        print("\n" + "=" * 80)
        print("✅ EJECUCIÓN COMPLETA FINALIZADA")
        print("=" * 80)
        
        self.pausar()
    
    def ejemplo_personalizado(self):
        """Permite al usuario ingresar sus propias palabras en lugar de longitudes"""
        print("\n EJEMPLO PERSONALIZADO")
        print("-" * 80)
    
        try:
            # Solicitar palabras reales
            print("\nIngresa las palabras separadas por espacios:")
            print("Ejemplo: casa perro gato universidad")
            texto = input("Palabras: ").strip()
        
            # Lista de palabras
            palabras_texto = texto.split()
            if not palabras_texto:
                print("\n❌ No ingresaste ninguna palabra.")
                self.pausar()
                return
        
            # Convertir palabras a longitudes (número de caracteres)
            palabras_longitudes = [len(p) for p in palabras_texto]
        
            print(f"\nPalabras ingresadas: {palabras_texto}")
            print(f"Longitudes usadas internamente: {palabras_longitudes}")
        
            # Pedir parámetros del modelo
            print("\nTen en cuenta que L es la longitud máxima de la línea en caracteres.")
            L = int(input("Longitud de línea (L): "))
            b = float(input("Amplitud ideal de espacios (b): "))
        
            print("\n Resolviendo con tus parámetros...")
            print(f"L = {L}, b = {b}")
        
            from division_parrafos import DivisionParrafos, mostrar_solucion
            import time
        
            dp = DivisionParrafos(palabras_longitudes, L, b)
        
            # Resolver con iterativo (el más eficiente)
            inicio = time.perf_counter()
            costo, cortes = dp.resolver_iterativo()
            tiempo = time.perf_counter() - inicio
        
            print(f"\n✅ SOLUCIÓN ENCONTRADA")
            print(f"Costo óptimo total: {costo:.4f}")
            print(f"Tiempo: {tiempo*1000:.4f} ms")
        
            # ----- Mostrar el texto formateado por líneas (con palabras reales) -----
            print("\nPárrafos formateados (con tus palabras):")
            print("-" * 80)
        
            lineas_info = []
            inicio_idx = 0
            for corte in cortes:
                # 'corte' es un índice 1-based del algoritmo
                fin_idx = corte
                linea_palabras = palabras_texto[inicio_idx:fin_idx]
                linea_texto = " ".join(linea_palabras)
                print(linea_texto)
            
                # Guardar info para el detalle por parámetros
                i = inicio_idx          # índice inicial 0-based
                j = fin_idx - 1         # índice final 0-based
                sum_long = sum(palabras_longitudes[i:fin_idx])
                num_pal_linea = fin_idx - inicio_idx
                num_espacios = max(num_pal_linea - 1, 0)
            
                # b' solo tiene sentido si hay al menos un espacio
                if num_espacios > 0:
                    b_prima = (L - sum_long) / num_espacios
                else:
                    b_prima = None
            
                costo_linea = dp.calcular_costo_linea(i, j)
            
                lineas_info.append({
                    "linea": len(lineas_info) + 1,
                    "palabras": linea_palabras,
                    "i": i,
                    "j": j,
                    "sum_long": sum_long,
                    "num_espacios": num_espacios,
                    "b_prima": b_prima,
                    "costo_linea": costo_linea,
                })
            
                inicio_idx = fin_idx
        
            print("-" * 80)
        
            # ----- Detalle por línea según los parámetros del modelo -----
            print("\nDetalle por línea (según L y b):")
            print("-" * 80)
            for info in lineas_info:
                print(f"Línea {info['linea']}:")
                print(f"  Palabras           : {' '.join(info['palabras'])}")
                print(f"  Índices (1-based)  : {info['i'] + 1} a {info['j'] + 1}")
                print(f"  Longitud palabras  : {info['sum_long']} caracteres")
                print(f"  Número de espacios : {info['num_espacios']}")
            
                if info['b_prima'] is not None:
                    print(f"  b' calculado       : {info['b_prima']:.4f}")
                else:
                    print("  b' calculado       : N/A (solo una palabra)")
            
                if info['costo_linea'] == float('inf'):
                    print("  Costo de la línea  : inf (no cabe en la longitud L)")
                else:
                    print(f"  Costo de la línea  : {info['costo_linea']:.4f}")
            
                print("-" * 80)
        
            # ----- Representación interna original (opcional) -----
            print("\nRepresentación interna (longitudes):")
            mostrar_solucion(palabras_longitudes, cortes, L, b)
        
        except ValueError:
            print("\n❌ Error: Entrada inválida. Usa números enteros/decimales para L y b.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
        self.pausar()

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
        print("\n📊 Generando análisis y gráficas del stress test (n grandes)...")
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
        print("\n\nPrograma interrumpido. ¡Hasta luego!")
        sys.exit(0)


if __name__ == "__main__":
    main()
