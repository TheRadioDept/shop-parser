import sqlite3
import os
import json
import pika

try:
    items_db = os.environ["itemsDB.db"]
except KeyError:
    items_db = "itemsDB.sqlite"
try:
    RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
except KeyError:
    RABBITMQ_HOST = "localhost"

try:
    RABBITMQ_QUEUE = os.environ["RABBITMQ_QUEUE"]
except KeyError:
    RABBITMQ_QUEUE = "item"


sqliteDB = sqlite3.connect(items_db)
cursor = sqliteDB.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS goods(
                    articul INT PRIMARY KEY NOT NULL,
                    name TEXT NOT NULL,
                    price TEXT,
                    category TEXT,
                    description TEXT,
                    photo_urls TEXT )"""
)

rabbitmq = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = rabbitmq.channel()
channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)


def callback(ch, method, properties, body):
    data = json.loads(body)
    info = cursor.execute("SELECT * FROM goods WHERE articul = ?", (data["articul"],))
    if not info.fetchone():
        cursor.execute(
            "INSERT INTO goods(articul, name, price, category, description, photo_urls) VALUES(?, ?, ?, ?, ?, ?)",
            (
                data["articul"],
                data["name"],
                data["price"],
                data["category"],
                data["description"],
                ", ".join(data["photo_urls"]),
            ),
        )
        sqliteDB.commit()


channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)

if __name__ == "__main__":
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
