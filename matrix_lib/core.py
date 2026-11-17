import asyncio
import numpy as np
from typing import List, Union
import httpx

# Изменяем интерфейс функции
async def get_matrix(url: str, use_numpy: bool = False) -> Union[List[int], np.ndarray]:
    """
    Асинхронно скачивает матрицу с сервера.
    :param use_numpy: Если True, возвращает результат как numpy array
    """
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            text = response.text
            matrix = parse_matrix(text)
            
            result_list = traverse_spiral_ccw(matrix)
            
            # Возвращаем numpy array, если это нужно смежной роли
            if use_numpy:
                return np.array(result_list)
            return result_list
            
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"Ошибка сервера: {e.response.status_code}") from e
    except httpx.RequestError as e:
        raise RuntimeError(f"Ошибка сети: {e}") from e

def parse_matrix(text: str) -> List[List[int]]:
    """Парсит текстовое представление матрицы со строгой проверкой типов."""
    rows = []
    for line in text.splitlines():
        if '|' in line:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            # Проверка: все ли элементы являются числами
            try:
                row = [int(x) for x in parts]
            except ValueError:
                raise ValueError(f"Ошибка парсинга: найдены нечисловые данные в строке: {line}")
            rows.append(row)
    
    # Проверка на квадратность (важно для корректного обхода спирали)
    if rows and len(set(len(r) for r in rows)) > 1:
        raise ValueError("Матрица не является квадратной или имеет рваные строки")
        
    return rows

def traverse_spiral_ccw(matrix: List[List[int]]) -> List[int]:
    """Обходит матрицу по спирали против часовой стрелки."""
    result = []
    if not matrix or not matrix[0]:
        return result
    
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # 1. Вниз по левой колонке
        for i in range(top, bottom + 1):
            result.append(matrix[i][left])
        left += 1
        
        # 2. Вправо по нижней строке
        if top <= bottom:
            for i in range(left, right + 1):
                result.append(matrix[bottom][i])
            bottom -= 1
            
        # 3. Вверх по правой колонке
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][right])
            right -= 1
            
        # 4. Влево по верхней строке
        if top <= bottom:
            for i in range(right, left - 1, -1):
                result.append(matrix[top][i])
            top += 1
            
    return result