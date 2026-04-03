import sqlite3

def check_database():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
      
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✓ Таблица 'users' существует в базе данных 'users'")
            
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"✓ Количество записей в таблице: {count}")
            
            if count > 0:
                print("\nСодержимое таблицы users:")
                cursor.execute("SELECT id, username, created_at FROM users")
                for row in cursor.fetchall():
                    print(f"  ID: {row[0]}, Логин: {row[1]}, Создан: {row[2]}")
        else:
            print("✗ Таблица 'users' не найдена")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")

if __name__ == '__main__':
    check_database()
