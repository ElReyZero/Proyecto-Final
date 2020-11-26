"""
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 * Hecho por:
 *
 * Juan Andrés Romero Colmenares - 202013449
 *
 """

def maxDicc(diccionario: dict):
    """Halla la llave con los valores máximos de un diccionario

    Args:
        diccionario (dict): Diccionario con los elementos
    """
    llaves = list(diccionario.keys())
    valores = list(diccionario.values())
    mayor = max(valores)
    Max = str(llaves[valores.index(mayor)])
    return Max

def minDicc(diccionario: dict):
    """Halla la llave con los valores minimos de un diccionario

    Args:
        diccionario (dict): Diccionario con los elementos
    """
    llaves = list(diccionario.keys())
    valores = list(diccionario.values())
    mayor = max(valores)
    Min = str(llaves[valores.index(mayor)])
    return Min