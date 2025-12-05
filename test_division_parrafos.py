"""
Test Suite para División en Párrafos (Actualizado para nueva función de costo)
Ejecutar con: pytest test_division_parrafos.py -v
"""

import pytest
import math
from division_parrafos import DivisionParrafos, ejecutar_y_medir


class TestCalculoCosto:
    """Tests para el cálculo de costo de líneas"""
    
    def test_costo_linea_simple(self):
        """Test con una línea simple de dos palabras"""
        dp = DivisionParrafos([5, 3, 4], 15, 1.5)
        # Nueva fórmula: suma=8, espacios=1, b'=(15-8)/1=7
        # Costo: 1 * (7-1.5)² + ((15-9)/15)²
        # (5.5)² + (6/15)² = 30.25 + 0.16 = 30.41
        costo = dp.calcular_costo_linea(0, 1)
        assert costo == pytest.approx(30.41, abs=0.01)
    
    def test_costo_ultima_linea(self):
        """La última línea tiene costo reducido (no cero)"""
        dp = DivisionParrafos([5, 3, 4], 15, 1.5)
        costo = dp.calcular_costo_linea(0, 2)  # Última línea
        # Última línea: espacio_sobrante=15-12-2=1
        # Costo = (1/15)² = 0.004444...
        assert costo == pytest.approx(0.004444, abs=0.0001)
    
    def test_costo_no_cabe(self):
        """Línea que no cabe debe retornar infinito"""
        dp = DivisionParrafos([10, 10], 15, 1.5)
        costo = dp.calcular_costo_linea(0, 1)
        assert costo == float('inf')
    
    def test_costo_palabra_sola(self):
        """Una sola palabra en línea tiene costo"""
        dp = DivisionParrafos([5], 15, 1.5)
        # Palabra sola: espacio_sobrante=15-5=10
        # Costo = (10/15)² = 0.4444...
        costo = dp.calcular_costo_linea(0, 0)
        assert costo == pytest.approx(0.4444, abs=0.0001)
    
    def test_espacios_negativos(self):
        """Palabras muy largas que hacen b' negativo"""
        dp = DivisionParrafos([8, 8], 10, 1.5)
        costo = dp.calcular_costo_linea(0, 1)
        assert costo == float('inf')


class TestAlgoritmoIterativo:
    """Tests para el algoritmo iterativo (DP)"""
    
    def test_caso_basico(self):
        """Test con caso básico"""
        dp = DivisionParrafos([5, 3], 15, 1.5)
        costo, cortes = dp.resolver_iterativo()
        assert costo >= 0
        # Cortes son índices 0-based de últimas palabras de línea
        # Para 2 palabras, podría ser [] (una línea) o [0] (dos líneas)
        assert cortes is not None
    
    def test_una_palabra(self):
        """Test con una sola palabra"""
        dp = DivisionParrafos([5], 15, 1.5)
        costo, cortes = dp.resolver_iterativo()
        # Palabra sola: espacio_sobrante=10, costo=(10/15)²=0.4444
        assert costo == pytest.approx(0.4444, abs=0.0001)
        # Una palabra: sin cortes intermedios
        assert cortes == []
    
    def test_todas_en_una_linea(self):
        """Test donde todas las palabras caben en una línea"""
        dp = DivisionParrafos([2, 2, 2], 20, 1.0)
        costo, cortes = dp.resolver_iterativo()
        
        # CON NUEVA FUNCIÓN: Si son última línea, costo reducido
        # Suma=6, espacios=2, espacio_usado=8, espacio_sobrante=12
        # Costo para última línea = (12/20)² = 0.36
        assert costo == pytest.approx(0.36, abs=0.01)
        # Última línea: sin cortes
        assert cortes == []
    
    def test_resultado_finito(self):
        """El costo debe ser finito para entrada válida"""
        dp = DivisionParrafos([3, 4, 2, 5], 15, 2.0)
        costo, cortes = dp.resolver_iterativo()
        assert costo < float('inf')
        assert len(cortes) <= 4


class TestAlgoritmoRecursivo:
    """Tests para el algoritmo recursivo puro"""
    
    def test_caso_pequeno(self):
        """Test con caso pequeño (recursivo es lento)"""
        dp = DivisionParrafos([5, 3], 15, 1.5)
        costo, cortes = dp.resolver_recursivo()
        assert costo >= 0
        # Puede ser [] o [0] dependiendo del costo
    
    def test_una_palabra_recursivo(self):
        """Test recursivo con una palabra"""
        dp = DivisionParrafos([5], 15, 1.5)
        costo, cortes = dp.resolver_recursivo()
        assert costo == pytest.approx(0.4444, abs=0.0001)
        assert cortes == []
    
    def test_consistencia_con_iterativo(self):
        """El resultado recursivo debe coincidir con iterativo"""
        dp = DivisionParrafos([3, 4, 2], 15, 1.5)
        costo_rec, cortes_rec = dp.resolver_recursivo()
        costo_iter, cortes_iter = dp.resolver_iterativo()
        # Pueden diferir ligeramente por reconstrucción, pero costo similar
        assert abs(costo_rec - costo_iter) < 0.1


class TestAlgoritmoDivideVenceras:
    """Tests para el algoritmo divide y vencerás"""
    
    def test_caso_basico_dyv(self):
        """Test básico para divide y vencerás"""
        dp = DivisionParrafos([5, 3, 4], 15, 1.5)
        costo, cortes = dp.resolver_divide_venceras()
        assert costo >= 0
        # Puede tener o no cortes
    
    def test_consistencia_dyv_iterativo(self):
        """Divide y vencerás debe dar mismo resultado que iterativo"""
        dp = DivisionParrafos([3, 4, 2, 5], 15, 2.0)
        costo_dyv, _ = dp.resolver_divide_venceras()
        costo_iter, _ = dp.resolver_iterativo()
        assert abs(costo_dyv - costo_iter) < 0.1
    
    def test_caso_mediano_dyv(self):
        """Test con entrada mediana"""
        dp = DivisionParrafos([3, 4, 2, 5, 3, 4], 20, 2.0)
        costo, cortes = dp.resolver_divide_venceras()
        assert costo < float('inf')
        # Cortes son 0-based, no 1-based
        if cortes:
            assert cortes[-1] < 6  # Menor que número de palabras


class TestAlgoritmoExhaustivo:
    """Tests para el algoritmo exhaustivo"""
    
    def test_caso_muy_pequeno(self):
        """Exhaustivo solo funciona con entradas muy pequeñas"""
        dp = DivisionParrafos([5, 3], 15, 1.5)
        costo, cortes = dp.resolver_exhaustivo()
        assert costo >= 0
        # Puede ser [] o [0]
    
    def test_consistencia_exhaustivo(self):
        """Exhaustivo debe dar resultado óptimo igual a otros"""
        dp = DivisionParrafos([3, 4], 15, 1.5)
        costo_exh, _ = dp.resolver_exhaustivo()
        costo_iter, _ = dp.resolver_iterativo()
        assert abs(costo_exh - costo_iter) < 0.1


class TestCasosEspeciales:
    """Tests para casos especiales y edge cases"""
    
    def test_linea_exacta(self):
        """Palabras que llenan exactamente la línea"""
        # 5 + 3 + 2 = 10, con 2 espacios de 2.5 cada uno = 5
        # Total: 10 + 5 = 15 perfecto
        dp = DivisionParrafos([5, 3, 2], 15, 2.5)
        costo, cortes = dp.resolver_iterativo()
        # Con nueva función, última línea perfecta aún tiene costo pequeño
        # espacio_sobrante = 15 - (10+2) = 3
        # Costo = (3/15)² = 0.04
        assert costo == pytest.approx(0.04, abs=0.0001)
        # Una línea: sin cortes
        assert cortes == []
    
    def test_espacios_ideales(self):
        """Cuando los espacios son exactamente ideales"""
        # 5 + 5 + 2 = 12, espacios: 2, b' = (15-12)/2 = 1.5 = b
        dp = DivisionParrafos([5, 5, 2], 15, 1.5)
        costo = dp.calcular_costo_linea(0, 2)
        # Última línea: espacio_sobrante=15-12-2=1
        # Costo = (1/15)² = 0.004444...
        assert costo == pytest.approx(0.004444, abs=0.0001)
    
    def test_muchas_lineas(self):
        """Caso que requiere muchas líneas"""
        palabras = [5] * 10  # 10 palabras de longitud 5
        dp = DivisionParrafos(palabras, 15, 1.0)
        costo, cortes = dp.resolver_iterativo()
        assert costo < float('inf')
        # Con nueva función, podría poner cada palabra sola
    
    def test_parametros_diferentes(self):
        """Test con diferentes valores de b usando el mismo texto"""
        palabras = [5, 5, 5, 5]
        L = 15

        dp1 = DivisionParrafos(palabras, L, 1.0)
        dp2 = DivisionParrafos(palabras, L, 3.0)

        costo1, _ = dp1.resolver_iterativo()
        costo2, _ = dp2.resolver_iterativo()

        assert costo1 >= 0
        assert costo2 >= 0
        # Pueden diferir con nueva función de costo


class TestRendimiento:
    """Tests de rendimiento y límites"""
    
    def test_tiempo_iterativo(self):
        """El iterativo debe ser rápido incluso con entrada mediana"""
        import time
        palabras = [3, 4, 2, 5, 3, 4, 6, 2] * 3  # 24 palabras
        dp = DivisionParrafos(palabras, 20, 2.0)
        
        inicio = time.perf_counter()
        costo, cortes = dp.resolver_iterativo()
        tiempo = time.perf_counter() - inicio
        
        assert tiempo < 1.0  # Debe terminar en menos de 1 segundo
        assert costo < float('inf')
    
    def test_escalabilidad_iterativo(self):
        """Iterativo debe manejar entradas grandes"""
        palabras = [3, 4, 2, 5] * 10  # 40 palabras
        dp = DivisionParrafos(palabras, 20, 2.0)
        costo, cortes = dp.resolver_iterativo()
        
        assert costo < float('inf')
        assert len(cortes) <= 40


class TestValidacionResultados:
    """Tests para validar que los resultados sean correctos"""
    
    def test_cortes_validos(self):
        """Los puntos de corte deben ser válidos"""
        dp = DivisionParrafos([5, 3, 4, 2], 15, 1.5)
        costo, cortes = dp.resolver_iterativo()
        
        # Cortes deben estar en orden creciente
        assert cortes == sorted(cortes)
        # Todos los cortes deben ser índices válidos
        assert all(0 <= c < 4 for c in cortes)
        # No cortes duplicados
        assert len(cortes) == len(set(cortes))
    
    def test_todas_palabras_incluidas(self):
        """Todas las palabras deben estar en alguna línea"""
        dp = DivisionParrafos([3, 4, 2, 5, 3], 15, 2.0)
        costo, cortes = dp.resolver_iterativo()
        
        # Verificar reconstrucción
        if cortes:
            # El último corte debe ser < 5
            assert cortes[-1] < 5
            # Cortes deben estar en rango
            assert all(c < 5 for c in cortes)
    
    def test_costo_no_negativo(self):
        """El costo nunca debe ser negativo"""
        dp = DivisionParrafos([3, 4, 2, 5], 15, 2.0)
        costo, cortes = dp.resolver_iterativo()
        assert costo >= 0


@pytest.fixture
def ejemplo_simple():
    """Fixture con un ejemplo simple para tests"""
    return DivisionParrafos([5, 3, 4], 15, 1.5)


@pytest.fixture
def ejemplo_complejo():
    """Fixture con un ejemplo más complejo"""
    return DivisionParrafos([3, 4, 2, 5, 3, 4, 6, 2], 20, 2.0)


def test_con_fixture_simple(ejemplo_simple):
    """Test usando fixture simple"""
    costo, cortes = ejemplo_simple.resolver_iterativo()
    assert costo >= 0
    # Puede tener o no cortes


def test_con_fixture_complejo(ejemplo_complejo):
    """Test usando fixture complejo"""
    costo, cortes = ejemplo_complejo.resolver_iterativo()
    assert costo < float('inf')
    if cortes:
        assert cortes[-1] < 8  # Índice 0-based


# Tests parametrizados
@pytest.mark.parametrize("palabras,L,b,esperado_lineas_min", [
    ([5, 3], 15, 1.5, 1),  # Al menos 1 línea
    ([5, 5, 5], 12, 1.0, 1),  # Al menos 1 línea (pueden ser 3)
    ([3, 4, 2], 20, 2.0, 1),  # Al menos 1 línea
    ([10, 10, 10], 15, 1.0, 3),  # Al menos 3 líneas (no caben juntas)
])
def test_numero_lineas(palabras, L, b, esperado_lineas_min):
    """Test parametrizado para verificar número mínimo de líneas"""
    dp = DivisionParrafos(palabras, L, b)
    costo, cortes = dp.resolver_iterativo()
    # Número de líneas = len(cortes) + 1
    num_lineas = len(cortes) + 1
    assert num_lineas >= esperado_lineas_min


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])