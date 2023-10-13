import redis

redis_db = redis.from_url("redis://localhost")

# создать запись в базе данных

redis_db.set("spam", 10)

data = redis_db.get("spam")
print(data)

redis_db.set("spam2", "hello", 60)
data2 = redis_db.get("spam2")
print(data2.decode())