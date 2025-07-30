# TZ_SHIFT — ETL

Проект предназначен для выполнения ETL-задач по команде с заданными параметрами дат. Реализует получение данных с API, обработку данных и загрузку в базу PostgreSQL.

## 🚀 Как выполнять команды

Для запуска ETL вручную

```
docker-compose run --rm app python main.py --start_date=2023-01-01 --end_date=2023-01-05
```

---

## База данных

Проект использует PostgreSQL.

*Скриншот терминала:*

![run command](images/img.png)


*Скрин таблицы в DBeaver:*

![db view](images/img_1.png)

*Скрин столбцов в DBeaver:*

![db columns](images/img_2.png)

