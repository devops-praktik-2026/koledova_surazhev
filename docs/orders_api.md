# Контракт API для Сервиса Заказов (Orders Service)

Документация описывает три обязательных запроса для работы с заказами.

---

## 1. Создание заказа
**POST** `/orders`

### Запрос (Request)
*   **Тело запроса (JSON):**
    ```json
    {
      "client_id": 1,
      "item_name": "Ноутбук",
      "quantity": 2
    }
    ```
*   **Обязательные поля:** `client_id`, `item_name`, `quantity` (должно быть не меньше 1).

### Ответы (Responses)
*   **Код 201 (Created)** — Заказ успешно создан:
    ```json
    {
      "order_id": 101,
      "client_id": 1,
      "item_name": "Ноутбук",
      "quantity": 2,
      "status": "created"
    }
    ```
*   **Код 422 (Unprocessable Entity)** — Ошибка валидации (нет обязательного поля или количество < 1):
    ```json
    {
      "detail": "Количество (quantity) должно быть не меньше 1"
    }
    ```
*   **Код 404 (Not Found)** — Указанный клиент не существует:
    ```json
    {
      "detail": "Клиент с ID 1 не найден"
    }
    ```

---

## 2. Получение заказа по номеру
**GET** `/orders/{order_id}`

### Ответы (Responses)
*   **Код 200 (OK)** — Заказ найден:
    ```json
    {
      "order_id": 101,
      "client_id": 1,
      "item_name": "Ноутбук",
      "quantity": 2,
      "status": "created"
    }
    ```
*   **Код 404 (Not Found)** — Заказ с таким номером не существует:
    ```json
    {
      "detail": "Заказ с номером 101 не найден"
    }
    ```

---

## 3. Список заказов клиента
**GET** `/orders/client/{client_id}`

### Параметры запроса (Query Parameters)
*   `limit` (integer, необязательный) — ограничение размера выдачи.

### Ответы (Responses)
*   **Код 200 (OK)** — Список заказов (если заказов нет, возвращается пустой список `[]`):
    ```json
    [
      {
        "order_id": 101,
        "client_id": 1,
        "item_name": "Ноутбук",
        "quantity": 2,
        "status": "created"
      }
    ]
    ```
