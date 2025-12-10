from app import app
from models import db, Item  # <--- ТЕПЕРЬ МЫ БЕРЕМ ИХ ИЗ models.py

if __name__ == '__main__':
    with app.app_context():
        # Получаем все товары
        items = Item.query.all()

        print("\n" + "=" * 50)
        print("   СОДЕРЖИМОЕ БАЗЫ ДАННЫХ (coursework.db)")
        print("=" * 50)
        print(f"{'ID':<5} | {'Name':<20} | {'Price':<10}")
        print("-" * 50)

        if not items:
            print("База данных пуста!")
        else:
            for item in items:
                print(f"{item.id:<5} | {item.name:<20} | {item.price:<10}")

        print("-" * 50 + "\n")