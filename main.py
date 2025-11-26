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
        print("\n🚀 Ejecutando casos de prueba...")
        print("-" * 80)
        
        from division_parrafos import ejecutar_comparacion
        ejecutar_comparacion()
        
        self.pausar()
    
    def ejecutar_analisis(self):
        """Ejecuta el análisis completo con gráficas"""
        print("\n📊 Ejecutando análisis de rendimiento...")
        print("-" * 80)
        
        from analisis_graficas import main as analisis_main
        analisis_main()
        
        self.pausar()
    
    def ejecutar_tests(self):
        """Ejecuta los tests con pytest"""
        print("\n🧪 Ejecutando tests con pytest...")
        print("-" * 80)
    
        # Usar el mismo intérprete de Python que ejecuta main.py
        resultado = subprocess.run(
            [sys.executable, '-m', 'pytest', 'test_division_parrafos.py', '-v', '--tb=short'],
            capture_output=False
        )
    
        if resultado.returncode == 0:
            print("\n✅ Todos los tests pasaron correctamente")
        else:
            print("\n❌ Algunos tests fallaron")
    
        self.pausar()

    
    def ejecutar_tests_cobertura(self):
        """Ejecuta tests con reporte de cobertura"""
        print("\n🧪 Ejecutando tests con cobertura...")
        print("-" * 80)
        
        # Verificar si pytest-cov está instalado
        try:
            import pytest_cov
            resultado = subprocess.run(
                ['pytest', 'test_division_parrafos.py', '-v', 
                 '--cov=division_parrafos', '--cov-report=term-missing'],
                capture_output=False
            )
            
            if resultado.returncode == 0:
                print("\n✅ Tests completados. Ver reporte de cobertura arriba.")
            
        except ImportError:
            print("\n⚠️  pytest-cov no está instalado.")
            print("Instala con: pip install pytest-cov")
        
        self.pausar()
    
    def ver_documentacion(self):
        """Muestra información del proyecto"""
        print("\n📚 DOCUMENTACIÓN DEL PROYECTO")
        print("=" * 80)
        
        print("""
Este proyecto implementa 4 algoritmos para el problema de División en Párrafos:

1. ITERATIVO (Programación Dinámica) - O(n²)
   ✅ Más eficiente, recomendado para producción
   
2. RECURSIVO PURO - O(2ⁿ)
   ⚠️  Exponencial, solo para demostración (n ≤ 10)
   
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
        print("\n🚀 EJECUCIÓN COMPLETA DEL PROYECTO")
        print("=" * 80)
        
        print("\n1️⃣  CASOS DE PRUEBA")
        print("-" * 80)
        self.ejecutar_casos_prueba()
        
        print("\n\n2️⃣  ANÁLISIS Y GRÁFICAS")
        print("-" * 80)
        self.ejecutar_analisis()
        
        print("\n\n3️⃣  TESTS UNITARIOS")
        print("-" * 80)
        self.ejecutar_tests()
        
        print("\n" + "=" * 80)
        print("✅ EJECUCIÓN COMPLETA FINALIZADA")
        print("=" * 80)
        
        self.pausar()
    
    def ejemplo_personalizado(self):
        """Permite al usuario ingresar sus propios datos"""
        print("\n✏️  EJEMPLO PERSONALIZADO")
        print("-" * 80)
        
        try:
            # Solicitar datos
            print("\nIngresa las longitudes de las palabras separadas por espacios:")
            print("Ejemplo: 5 3 4 6 2")
            palabras_str = input("Palabras: ").strip()
            palabras = [int(x) for x in palabras_str.split()]
            
            L = int(input("\nLongitud de línea (L): "))
            b = float(input("Amplitud ideal de espacios (b): "))
            
            print("\n🔍 Resolviendo con tus parámetros...")
            print(f"Palabras: {palabras}")
            print(f"L = {L}, b = {b}")
            
            from division_parrafos import DivisionParrafos, mostrar_solucion
            import time
            
            dp = DivisionParrafos(palabras, L, b)
            
            # Resolver con iterativo (el más eficiente)
            inicio = time.perf_counter()
            costo, cortes = dp.resolver_iterativo()
            tiempo = time.perf_counter() - inicio
            
            print(f"\n✅ SOLUCIÓN ENCONTRADA")
            print(f"Costo óptimo: {costo:.4f}")
            print(f"Tiempo: {tiempo*1000:.4f} ms")
            
            mostrar_solucion(palabras, cortes, L, b)
            
        except ValueError:
            print("\n❌ Error: Entrada inválida. Usa números enteros/decimales.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        self.pausar()
    
    def pausar(self):
        """Pausa la ejecución esperando input del usuario"""
        input("\n📌 Presiona ENTER para continuar...")
    
    def ejecutar(self):
        """Ejecuta el menú principal"""
        while True:
            self.mostrar_menu()
            
            opcion = input("\nOpción: ").strip()
            
            if opcion == '0':
                print("\n👋 ¡Hasta luego!")
                sys.exit(0)
            
            if opcion in self.opciones:
                _, funcion = self.opciones[opcion]
                if funcion:
                    try:
                        funcion()
                    except KeyboardInterrupt:
                        print("\n\n⚠️  Operación cancelada por el usuario")
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
        print("\n⚠️  ADVERTENCIA: Faltan dependencias")
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
        print("\n\n👋 Programa interrumpido. ¡Hasta luego!")
        sys.exit(0)


if __name__ == "__main__":
    main()