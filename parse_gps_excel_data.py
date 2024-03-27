import asyncio
from services import load_data_from_excel

# Путь к файлу Excel с данными GPS
file_path = "data/2_5420464171701519891.xlsx"

# Запускаем функцию загрузки данных из Excel в базу данных
async def main():
    await load_data_from_excel(file_path)

# Запускаем основную функцию
asyncio.run(main())
