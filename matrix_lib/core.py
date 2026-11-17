import asyncio
from typing import List
import httpx

async def get_matrix(url: str) -> List[int]:
    """
    Асинхронно скачивает матрицу с сервера и возвращает список элементов,
    обойденных по спирали против часовой стрелки.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            
            text = response.text
            matrix = parse_matrix(text)
            
            return traverse_spiral_ccw(matrix)
            
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"Ошибка сервера: {e.response.status_code}") from e
    except httpx.RequestError as e:
        raise RuntimeError(f"Ошибка сети: {e}") from e

def parse_matrix(text: str) -> List[List[int]]:
    """Парсит текстовое представление матрицы."""
    rows = []
    for line in text.splitlines():
        if '|' in line:
            # Убираем границы и лишние пробелы
            parts = [p.strip() for p in line.split('|')[1:-1]]
            row = [int(x) for x in parts]
            rows.append(row)
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