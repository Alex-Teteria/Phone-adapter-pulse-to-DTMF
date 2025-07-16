
import json

filename = "phone_directory.json"

# як приклад
phone_directory = {'01': '671234567',
                   '02': '987654321',
                   }

with open(filename, "w") as f:
    json.dump(phone_directory, f)
print(f"Словник записано у файл {filename}")


with open(filename, 'r', encoding='utf-8') as f:
      data = json.load(f)

print(data)

      

