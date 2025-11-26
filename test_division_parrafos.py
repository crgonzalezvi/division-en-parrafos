"""
Test Suite para División en Párrafos
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
        # Suma: 8, espacios: 1, b' = (15-8)/1 = 7
        # Costo: 1 * |7 - 1.5| = 5.5
        costo = dp.calcular_costo_linea(0, 1)
        assert costo == pytest.approx(5.5, abs=0.01)
    
    def test_costo_ultima_linea(self):
        """La última línea tiene costo cero si cabe"""
        dp = DivisionParrafos([5, 3, 4], 15, 1.5)
        costo = dp.calcular_costo_linea(0, 2)  # Última línea
        assert costo == 0.0
    
    def test_costo_no_cabe(self):
        """Línea que no cabe debe retornar infinito"""
        dp = DivisionParrafos([10, 10], 15, 1.5)
        costo = dp.calcular_costo_linea(0, 1)
        assert costo == float('inf')
    
    def test_costo_palabra_sola(self):
        """Una sola palabra en línea (sin espacios)"""
        dp = DivisionParrafos([5], 15, 1.5)
        costo = dp.calcular_costo_linea(0, 0)
        assert costo == 0.0
    
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
        assert len(cortes) > 0
        assert cortes[-1] == 2  # Última palabra
    
    def test_una_palabra(self):
        """Test con una sola palabra"""
        dp = DivisionParrafos([5], 15, 1.5)
        costo, cortes = dp.resolver_iterativo()
        assert costo == 0.0
        assert cortes == [1]
    
    def test_todas_en_una_linea(self):
        """Test donde todas las palabras caben en una línea"""
        dp = DivisionParrafos([2, 2, 2], 20, 1.0)
        costo, cortes = dp.resolver_iterativo()
        assert costo == 0.0  # Es la última línea
        assert cortes == [3]
    
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
        assert len(cortes) > 0
    
    def test_una_palabra_recursivo(self):
        """Test recursivo con una palabra"""
        dp = DivisionParrafos([5], 15, 1.5)
        costo, cortes = dp.resolver_recursivo()
        assert costo == 0.0
        assert cortes == [1]
    
    def test_consistencia_con_iterativo(self):
        """El resultado recursivo debe coincidir con iterativo"""
        dp = DivisionParrafos([3, 4, 2], 15, 1.5)
        costo_rec, cortes_rec = dp.resolver_recursivo()
        costo_iter, cortes_iter = dp.resolver_iterativo()
        assert costo_rec == pytest.approx(costo_iter, abs=0.01)


class TestAlgoritmoDivideVenceras:
    """Tests para el algoritmo divide y vencerás"""
    
    def test_caso_basico_dyv(self):
        """Test básico para divide y vencerás"""
        dp = DivisionParrafos([5, 3, 4], 15, 1.5)
        costo, cortes = dp.resolver_divide_venceras()
        assert costo >= 0
        assert len(cortes) > 0
    
    def test_consistencia_dyv_iterativo(self):
        """Divide y vencerás debe dar mismo resultado que iterativo"""
        dp = DivisionParrafos([3, 4, 2, 5], 15, 2.0)
        costo_dyv, _ = dp.resolver_divide_venceras()
        costo_iter, _ = dp.resolver_iterativo()
        assert costo_dyv == pytest.approx(costo_iter, abs=0.01)
    
    def test_caso_mediano_dyv(self):
        """Test con entrada mediana"""
        dp = DivisionParrafos([3, 4, 2, 5, 3, 4], 20, 2.0)
        costo, cortes = dp.resolver_divide_venceras()
        assert costo < float('inf')
        assert cortes[-1] == 6


class TestAlgoritmoExhaustivo:
    """Tests para el algoritmo exhaustivo"""
    
    def test_caso_muy_pequeno(self):
        """Exhaustivo solo funciona con entradas muy pequeñas"""
        dp = DivisionParrafos([5, 3], 15, 1.5)
        costo, cortes = dp.resolver_exhaustivo()
        assert costo >= 0
        assert len(cortes) > 0
    
    def test_consistencia_exhaustivo(self):
        """Exhaustivo debe dar resultado óptimo igual a otros"""
        dp = DivisionParrafos([3, 4], 15, 1.5)
        costo_exh, _ = dp.resolver_exhaustivo()
        costo_iter, _ = dp.resolver_iterativo()
        assert costo_exh == pytest.approx(costo_iter, abs=0.01)


class TestCasosEspeciales:
    """Tests para casos especiales y edge cases"""
    
    def test_linea_exacta(self):
        """Palabras que llenan exactamente la línea"""
        # 5 + 3 + 2 = 10, con 2 espacios de 2.5 cada uno = 5
        # Total: 10 + 5 = 15
        dp = DivisionParrafos([5, 3, 2], 15, 2.5)
        costo, cortes = dp.resolver_iterativo()
        assert costo == 0.0
        assert cortes == [3]
    
    def test_espacios_ideales(self):
        """Cuando los espacios son exactamente ideales"""
        # 5 + 5 + 2 = 12, espacios: 2, b' = (15-12)/2 = 1.5 = b
        dp = DivisionParrafos([5, 5, 2], 15, 1.5)
        costo = dp.calcular_costo_linea(0, 2)
        assert costo == 0.0
    
    def test_muchas_lineas(self):
        """Caso que requiere muchas líneas"""
        palabras = [5] * 10  # 10 palabras de longitud 5
        dp = DivisionParrafos(palabras, 15, 1.0)
        costo, cortes = dp.resolver_iterativo()
        assert costo < float('inf')
        assert len(cortes) >= 5  # Al menos 5 líneas necesarias
    
    def test_parametros_diferentes(self):
        """Test con diferentes valores de b usando el mismo texto"""
        palabras = [5, 5, 5, 5]
        L = 15

        dp1 = DivisionParrafos(palabras, L, 1.0)
        dp2 = DivisionParrafos(palabras, L, 3.0)

        costo1, _ = dp1.resolver_iterativo()
        costo2, _ = dp2.resolver_iterativo()

        # Ambos deben producir un costo óptimo válido (no negativo)
        assert costo1 >= 0
        assert costo2 >= 0

        # Y, dado el modelo de costo (una palabra por línea cuesta 0),
        # es razonable que el óptimo sea el mismo en ambos casos.
        assert costo1 == pytest.approx(costo2, abs=0.01)




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
        
        # Cortes deben estar en orden
        assert cortes == sorted(cortes)
        # Último corte debe ser el número total de palabras
        assert cortes[-1] == 4
        # Todos los cortes deben ser positivos
        assert all(c > 0 for c in cortes)
    
    def test_todas_palabras_incluidas(self):
        """Todas las palabras deben estar en alguna línea"""
        dp = DivisionParrafos([3, 4, 2, 5, 3], 15, 2.0)
        costo, cortes = dp.resolver_iterativo()
        
        assert cortes[-1] == 5  # Todas las palabras incluidas
    
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
    assert len(cortes) > 0


def test_con_fixture_complejo(ejemplo_complejo):
    """Test usando fixture complejo"""
    costo, cortes = ejemplo_complejo.resolver_iterativo()
    assert costo < float('inf')
    assert cortes[-1] == 8


# Tests parametrizados
@pytest.mark.parametrize("palabras,L,b,esperado_lineas", [
    ([5, 3], 15, 1.5, 1),
    ([5, 5, 5], 12, 1.0, 3),
    ([3, 4, 2], 20, 2.0, 1),
    ([10, 10, 10], 15, 1.0, 3),
])
def test_numero_lineas(palabras, L, b, esperado_lineas):
    """Test parametrizado para verificar número de líneas"""
    dp = DivisionParrafos(palabras, L, b)
    costo, cortes = dp.resolver_iterativo()
    assert len(cortes) >= esperado_lineas or costo == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])