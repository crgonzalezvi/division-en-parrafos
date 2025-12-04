"""
Módulo de análisis y generación de gráficas para División en Párrafos
Requiere: matplotlib, numpy
Instalar con: pip install matplotlib numpy
"""

import time
import matplotlib.pyplot as plt
import numpy as np
from typing import List
from division_parrafos import DivisionParrafos
import json
import math



class AnalizadorRendimiento:
    """Clase para analizar y comparar el rendimiento de los algoritmos"""
    
    def __init__(self):
        self.resultados = []
    
    def ejecutar_benchmark(self, tamaños: List[int], L: int = 20, b: float = 2.0):
        """
        Ejecuta benchmarks para diferentes tamaños de entrada.
        
        Args:
            tamaños: Lista de tamaños de entrada a probar
            L: Longitud de línea
            b: Amplitud ideal de espacios
        """
        print("=" * 80)
        print("BENCHMARK: Análisis de Rendimiento por Tamaño de Entrada")
        print("=" * 80)
        
        for n in tamaños:
            print(f"\nProbando con n={n} palabras...")
            
            # Generar palabras aleatorias pero reproducibles
            np.random.seed(42)
            palabras = np.random.randint(2, 8, size=n).tolist()
            
            dp = DivisionParrafos(palabras, L, b)
            
            resultado = {
                'n': n,
                'algoritmos': {}
            }
            
            # Iterativo (siempre ejecutar)
            print(" Ejecutando Iterativo...")
            inicio = time.perf_counter()
            costo_iter, _ = dp.resolver_iterativo()
            tiempo_iter = time.perf_counter() - inicio
            resultado['algoritmos']['Iterativo'] = {
                'tiempo': tiempo_iter,
                'costo': costo_iter
            }
            print(f"     ✓ Completado en {tiempo_iter*1000:.2f} ms")
            
            # Divide y Vencerás (siempre ejecutar)
            print("  Ejecutando Divide y Vencerás...")
            inicio = time.perf_counter()
            costo_dyv, _ = dp.resolver_divide_venceras()
            tiempo_dyv = time.perf_counter() - inicio
            resultado['algoritmos']['Divide y Vencerás'] = {
                'tiempo': tiempo_dyv,
                'costo': costo_dyv
            }
            print(f"     ✓ Completado en {tiempo_dyv*1000:.2f} ms")
            
            # Recursivo (solo para n pequeño)
            if n <= 8:
                print("   Ejecutando Recursivo Puro...")
                inicio = time.perf_counter()
                costo_rec, _ = dp.resolver_recursivo()
                tiempo_rec = time.perf_counter() - inicio
                resultado['algoritmos']['Recursivo'] = {
                    'tiempo': tiempo_rec,
                    'costo': costo_rec
                }
                print(f"     ✓ Completado en {tiempo_rec*1000:.2f} ms")
            else:
                print("    Recursivo omitido (n demasiado grande)")
            
            # Exhaustivo (solo para n muy pequeño)
            if n <= 5:
                print("    Ejecutando Exhaustivo...")
                inicio = time.perf_counter()
                costo_exh, _ = dp.resolver_exhaustivo()
                tiempo_exh = time.perf_counter() - inicio
                resultado['algoritmos']['Exhaustivo'] = {
                    'tiempo': tiempo_exh,
                    'costo': costo_exh
                }
                print(f"     ✓ Completado en {tiempo_exh*1000:.2f} ms")
            else:
                print("      Exhaustivo omitido (n demasiado grande)")
            
            self.resultados.append(resultado)
    
    def generar_graficas(self, guardar: bool = True, filename: str = 'analisis_division_parrafos.png'):
        """Genera todas las gráficas de análisis"""
        if not self.resultados:
            print("❌ No hay resultados para graficar. Ejecuta benchmark primero.")
            return
        
        # Configuración general
        plt.style.use('seaborn-v0_8-darkgrid')
        plt.figure(figsize=(16, 12))
        
        # 1. Gráfica de tiempo vs tamaño (escala logarítmica)
        ax1 = plt.subplot(2, 3, 1)
        self._grafica_tiempo_vs_n(ax1, log_scale=True)
        
        # 2. Gráfica de tiempo vs tamaño (escala lineal)
        ax2 = plt.subplot(2, 3, 2)
        self._grafica_tiempo_vs_n(ax2, log_scale=False)
        
        # 3. Comparación de costos
        ax3 = plt.subplot(2, 3, 3)
        self._grafica_comparacion_costos(ax3)
        
        # 4. Speedup relativo
        ax4 = plt.subplot(2, 3, 4)
        self._grafica_speedup(ax4)
        
        # 5. Tiempo acumulado
        ax5 = plt.subplot(2, 3, 5)
        self._grafica_tiempo_acumulado(ax5)
        
        # 6. Comparación Valor vs Bits
        ax6 = plt.subplot(2, 3, 6)
        self._grafica_valor_vs_bits(ax6)
        
        plt.tight_layout()
        
        if guardar:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"\n✅ Gráfica guardada como '{filename}'")
        
        plt.show()
    
    def _grafica_tiempo_vs_n(self, ax, log_scale: bool = False):
        """Gráfica de tiempo de ejecución vs tamaño de entrada"""
        algoritmos = {}
        
        for res in self.resultados:
            for alg_nombre, alg_datos in res['algoritmos'].items():
                if alg_nombre not in algoritmos:
                    algoritmos[alg_nombre] = {'n': [], 'tiempo': []}
                algoritmos[alg_nombre]['n'].append(res['n'])
                algoritmos[alg_nombre]['tiempo'].append(alg_datos['tiempo'] * 1000)  # ms
        
        colores = {
            'Iterativo': '#2ecc71',
            'Divide y Vencerás': '#3498db',
            'Recursivo': '#e74c3c',
            'Exhaustivo': '#9b59b6'
        }
        
        for alg_nombre, datos in algoritmos.items():
            ax.plot(
                datos['n'], datos['tiempo'],
                marker='o', linewidth=2, markersize=8,
                label=alg_nombre, color=colores.get(alg_nombre, 'gray')
            )
        
        if log_scale:
            ax.set_yscale('log')
            ax.set_title('Tiempo de Ejecución vs Tamaño (Escala Log)', fontsize=12, fontweight='bold')
        else:
            ax.set_title('Tiempo de Ejecución vs Tamaño (Escala Lineal)', fontsize=12, fontweight='bold')
        
        ax.set_xlabel('Número de palabras (n)', fontsize=10)
        ax.set_ylabel('Tiempo (ms)', fontsize=10)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _grafica_comparacion_costos(self, ax):
        """Gráfica comparando que todos dan (idealmente) el mismo costo óptimo"""
        n_values = []
        costos = []

        for res in self.resultados:
            algs = res.get('algoritmos', {})
            if not algs:
                continue

            # Tomamos el primer algoritmo para obtener el costo
            alg_datos = next(iter(algs.values()), None)
            if alg_datos is None:
                continue

            costo = alg_datos.get('costo', None)
            if costo is None:
                continue

            n_values.append(res['n'])
            costos.append(float(costo))

        # Si no hay datos, mostramos un mensaje en la gráfica
        if not n_values or not costos:
            ax.text(
                0.5, 0.5, "Sin datos de costo",
                ha='center', va='center', transform=ax.transAxes
            )
            ax.set_title('Costo Óptimo por Tamaño de Entrada', fontsize=12, fontweight='bold')
            return

        # Asegurar que ambas listas tengan la misma longitud
        min_len = min(len(n_values), len(costos))
        n_values = n_values[:min_len]
        costos = costos[:min_len]

        x = np.arange(min_len)
        costos = np.array(costos)

        ax.bar(x, costos, color='#2ecc71', alpha=0.8, label='Costo Óptimo')
    
        ax.set_xlabel('Número de palabras (n)', fontsize=10)
        ax.set_ylabel('Costo óptimo', fontsize=10)
        ax.set_title('Costo Óptimo por Tamaño de Entrada', fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(n_values)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

    def _grafica_speedup(self, ax):
        """Gráfica de speedup del iterativo vs otros algoritmos"""
        n_values = []
        speedups = {'Recursivo': [], 'Exhaustivo': [], 'Divide y Vencerás': []}
        
        for res in self.resultados:
            if 'Iterativo' not in res['algoritmos']:
                continue
            
            n_values.append(res['n'])
            tiempo_iter = res['algoritmos']['Iterativo']['tiempo']
            
            for alg_nombre in ['Recursivo', 'Exhaustivo', 'Divide y Vencerás']:
                if alg_nombre in res['algoritmos']:
                    tiempo_alg = res['algoritmos'][alg_nombre]['tiempo']
                    speedup = tiempo_alg / tiempo_iter if tiempo_iter > 0 else 0
                    speedups[alg_nombre].append(speedup)
                else:
                    speedups[alg_nombre].append(None)
        
        for alg_nombre, valores in speedups.items():
            # Filtrar Nones
            n_filtrado = [n for n, v in zip(n_values, valores) if v is not None]
            v_filtrado = [v for v in valores if v is not None]
            
            if v_filtrado:
                ax.plot(
                    n_filtrado, v_filtrado,
                    marker='o', linewidth=2, markersize=8,
                    label=f'{alg_nombre}'
                )
        
        ax.axhline(
            y=1, color='red',
            linestyle='--', linewidth=2,
            label='Baseline (Iterativo)'
        )
        ax.set_xlabel('Número de palabras (n)', fontsize=10)
        ax.set_ylabel('Speedup (veces más lento que Iterativo)', fontsize=10)
        ax.set_title('Speedup Relativo vs Iterativo', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')
    
    def _grafica_tiempo_acumulado(self, ax):
        """Gráfica de comparación de tiempos de los algoritmos principales"""
        n_values = []
        iter_tiempos = []
        dyv_tiempos = []
    
        for res in self.resultados:
            n_values.append(res['n'])
        
            if 'Iterativo' in res['algoritmos']:
                iter_tiempos.append(res['algoritmos']['Iterativo']['tiempo'] * 1000)
            else:
                iter_tiempos.append(0)
        
            if 'Divide y Vencerás' in res['algoritmos']:
                dyv_tiempos.append(res['algoritmos']['Divide y Vencerás']['tiempo'] * 1000)
            else:
                dyv_tiempos.append(0)
    
        width = 0.35
        x = np.arange(len(n_values))
    
        ax.bar(
            x - width/2, iter_tiempos, width,
            label='Iterativo', color='#2ecc71', alpha=0.8
        )
        ax.bar(
            x + width/2, dyv_tiempos, width,
            label='Divide y Vencerás', color='#3498db', alpha=0.8
        )
    
        ax.set_xlabel('Número de palabras (n)', fontsize=10)
        ax.set_ylabel('Tiempo (ms)', fontsize=10)
        ax.set_title('Comparación de Tiempos - Algoritmos Eficientes', fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(n_values)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
    
   
    def _grafica_valor_vs_bits(self, ax):
        """Gráfica comparando complejidad por valor vs bits"""
        n_values = []
        ops_valor = []
        ops_bits = []
        tiempo_real = []
        
        for res in self.resultados:
            n = res['n']
            bits = math.ceil(math.log2(n)) if n > 0 else 1
            
            n_values.append(n)
            ops_valor.append(n * n)
            ops_bits.append(2 ** (2 * bits))
            
            if 'Iterativo' in res['algoritmos']:
                tiempo_real.append(res['algoritmos']['Iterativo']['tiempo'] * 1000)
        
        # Normalizar para comparación visual
        max_ops = max(max(ops_valor), max(ops_bits))
        ops_valor_norm = [o / max_ops * 100 for o in ops_valor]
        ops_bits_norm = [o / max_ops * 100 for o in ops_bits]
        
        x = np.arange(len(n_values))
        width = 0.25
        
        ax.bar(x - width, ops_valor_norm, width, label='O(n²) - Por Valor', 
              color='#2ecc71', alpha=0.8)
        ax.bar(x, ops_bits_norm, width, label='O(2^(2b)) - Por Bits', 
              color='#e74c3c', alpha=0.8)
        
        # Tiempo real como línea
        ax2 = ax.twinx()
        ax2.plot(x, tiempo_real, 'o-', color='#3498db', linewidth=2, 
                markersize=6, label='Tiempo Real')
        
        ax.set_xlabel('Número de palabras (n)', fontsize=10)
        ax.set_ylabel('Operaciones Teóricas (% normalizado)', fontsize=10)
        ax2.set_ylabel('Tiempo Real (ms)', fontsize=10, color='#3498db')
        ax.set_title('Complejidad: Valor vs Bits vs Tiempo Real', 
                    fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(n_values)
        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')
        ax.grid(True, alpha=0.3)

    def generar_tabla_comparativa(self):
        """Genera una tabla comparativa de resultados"""
        print("\n" + "=" * 120)
        print("TABLA COMPARATIVA DE RENDIMIENTO (Análisis Dual: Valor y Bits)")
        print("=" * 120)
        
        print(f"\n{'n':<5} | {'bits':<6} | {'Algoritmo':<20} | {'Tiempo(ms)':<12} | "
              f"{'Costo':<10} | {'Comp.Valor':<15} | {'Comp.Bits':<15}")
        print("-" * 120)
        
        for res in self.resultados:
            n = res['n']
            bits = math.ceil(math.log2(n)) if n > 0 else 1
            
            for alg_nombre, alg_datos in sorted(res['algoritmos'].items()):
                tiempo_ms = alg_datos['tiempo'] * 1000
                costo = alg_datos['costo']
                
                # Determinar complejidades según algoritmo
                if 'Iterativo' in alg_nombre or 'Divide' in alg_nombre:
                    comp_valor = "O(n²)"
                    comp_bits = "O(2^(2b))"
                elif 'Recursivo' in alg_nombre:
                    comp_valor = "O(2^n)"
                    comp_bits = "O(2^(2^b))"
                else:  # Exhaustivo
                    comp_valor = "O(B(n))"
                    comp_bits = "O(B(2^b))"
                
                print(f"{n:<5} | {bits:<6} | {alg_nombre:<20} | {tiempo_ms:>10.4f} | "
                      f"{costo:>8.4f} | {comp_valor:<15} | {comp_bits:<15}")
            
            print("-" * 120)
    
    def analisis_complejidad_dual(self):
        """Genera análisis comparando perspectiva de valor vs bits"""
        
        print("\n" + "=" * 100)
        print("ANÁLISIS DE COMPLEJIDAD: PERSPECTIVA VALOR vs BITS")
        print("=" * 100)
        
        print("\nEste análisis muestra la diferencia entre medir complejidad por:")
        print("  • VALOR: Número de elementos (n)")
        print("  • BITS: Tamaño de representación binaria (b = log₂(n))")
        print()
        
        print(f"{'n':<8} {'bits(b)':<10} {'O(n²)':<15} {'O(2^(2b))':<15} {'Ratio':<12} {'Tiempo(ms)':<12}")
        print("-" * 100)
        
        for res in self.resultados:
            n = res['n']
            bits = math.ceil(math.log2(n)) if n > 0 else 1
            
            ops_valor = n * n
            ops_bits = 2 ** (2 * bits)
            ratio = ops_bits / ops_valor
            
            if 'Iterativo' in res['algoritmos']:
                tiempo = res['algoritmos']['Iterativo']['tiempo'] * 1000
                print(f"{n:<8} {bits:<10} {ops_valor:<15,} {ops_bits:<15,} {ratio:<12.2f} {tiempo:<12.4f}")
        
        print("\nINTERPRETACIÓN:")
        print("-" * 100)
        print("El Ratio muestra cuántas veces más operaciones se requieren al medir por bits.")
        print("Aunque O(n²) parece polinomial, O(2^(2b)) es exponencial en el tamaño real.")
        print("Esto clasifica al problema como PSEUDO-POLINOMIAL, no verdaderamente polinomial.")
    
    
    def guardar_resultados_json(self, filename: str = 'resultados_benchmark.json'):
        """Guarda los resultados en formato JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Resultados guardados en '{filename}'")
    
    def generar_informe_completo(self):
        """Genera un informe completo en texto"""
        print("\n" + "=" * 100)
        print("INFORME COMPLETO DE ANÁLISIS")
        print("=" * 100)
        
        print("\nCOMPLEJIDAD TEÓRICA:")
        print("-" * 100)
        print(f"{'Algoritmo':<25} | {'Tiempo':<15} | {'Espacio':<15} | {'Características'}")
        print("-" * 100)
        print(f"{'Iterativo (DP)':<25} | {'O(n²)':<15} | {'O(n)':<15} | Óptimo, bottom-up")
        print(f"{'Recursivo Puro':<25} | {'O(2ⁿ)':<15} | {'O(n)':<15} | Exponencial, sin memo")
        print(f"{'Divide y Vencerás':<25} | {'O(n²)':<15} | {'O(n²)':<15} | Con memoización")
        print(f"{'Exhaustivo':<25} | {'O(B(n))':<15} | {'O(n)':<15} | Bell number, muy lento")
        
        print("\nANÁLISIS DE RESULTADOS EXPERIMENTALES:")
        print("-" * 100)
        
        # Calcular promedios
        if self.resultados:
            iter_times = []
            dyv_times = []
            
            for res in self.resultados:
                if 'Iterativo' in res['algoritmos']:
                    iter_times.append(res['algoritmos']['Iterativo']['tiempo'])
                if 'Divide y Vencerás' in res['algoritmos']:
                    dyv_times.append(res['algoritmos']['Divide y Vencerás']['tiempo'])
            
            if iter_times:
                print(f"Tiempo promedio Iterativo: {np.mean(iter_times)*1000:.4f} ms")
            if dyv_times:
                print(f"Tiempo promedio Divide y Vencerás: {np.mean(dyv_times)*1000:.4f} ms")
            
            if iter_times and dyv_times:
                ratio = np.mean(dyv_times) / np.mean(iter_times)
                print(f"Ratio D&V/Iterativo: {ratio:.2f}x")
        
        print("\n✅ CONCLUSIONES:")
        print("-" * 100)
        print("1. El algoritmo ITERATIVO (Programación Dinámica) es el más eficiente")
        print("2. Recursivo puro es impracticable para n > 10")
        print("3. Exhaustivo solo sirve para demostración con n <= 5")
        print("4. Divide y Vencerás tiene rendimiento similar a Iterativo pero más overhead")
        print("5. Para producción: usar ITERATIVO")


def main():
    """Función principal para ejecutar análisis completo"""
    print("Iniciando análisis completo de rendimiento...")
    
    analizador = AnalizadorRendimiento()
    
    # Definir tamaños a probar
    # Pequeños: incluyen todos los algoritmos
    # Medianos/grandes: solo algoritmos eficientes
    tamaños = [3, 5, 8, 10, 15, 20, 30, 40]
    
    print(f"\nTamaños a probar: {tamaños}")
    print("Nota: Algoritmos lentos se omitirán automáticamente en entradas grandes\n")
    
    # Ejecutar benchmark
    analizador.ejecutar_benchmark(tamaños, L=20, b=2.0)
    
    # Generar tabla comparativa
    analizador.generar_tabla_comparativa()
    
    # Generar informe
    analizador.generar_informe_completo()
    
    # Guardar resultados
    analizador.guardar_resultados_json()
    
    # Generar gráficas
    print("\nGenerando gráficas...")
    analizador.generar_graficas(guardar=True, filename='analisis_division_parrafos.png')
    
    print("\n" + "=" * 100)
    print("✅ANÁLISIS COMPLETO FINALIZADO")
    print("=" * 100)
    print("\nArchivos generados:")
    print("  - analisis_division_parrafos.png (gráficas)")
    print("  - resultados_benchmark.json (datos en JSON)")


if __name__ == "__main__":
    main()
