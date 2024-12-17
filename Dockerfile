# 1. Asosiy imidj (bazaviy tizimni belgilash)
FROM python:3.11-slim

# 2. Ishlash papkasini belgilash
WORKDIR /app

# 3. Talablarni o'rnatish
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 4. Loyiha fayllarini konteynerga nusxalash
COPY . .

# 5. Konteynerda bajariladigan buyruq
CMD ["python", "main.py"]
