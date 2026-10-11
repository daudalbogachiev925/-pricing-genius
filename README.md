# -pricing-genius
Описание: платформа оптимального ценообразования. Модели спроса (линейная и log-log), эластичность, A/B-тесты, сегментация, симулятор прибыли, отчёт.  Стек: Python, FastAPI, PostgreSQL, SciPy, statsmodels, Streamlit, Docker.

# pricing-genius

Платформа оптимального ценообразования с моделями спроса, эластичностью, A/B-тестами и сегментацией.

## Возможности
- Хранение A/B-наблюдений (price, quantity, segment)
- Модели спроса: линейная и log-log (power law)
- Точечная эластичность
- Оптимизация цены: max revenue или max profit
- A/B-тест с t-статистикой и p-value
- Сегментация: economy / mid / premium
- Симулятор реакции конкурента
- Streamlit-дашборд

## Быстрый старт

cp .env.example .env
docker-compose up --build

API: http://localhost:8000/docs
Dashboard: http://localhost:8501

## Пример

for p in 60 80 100 120 140 160; do
  q=$((1000 - 4*p))
  curl -X POST http://localhost:8000/api/ab-data \
    -H "Content-Type: application/json" \
    -d "{\"experiment_id\":\"e1\",\"price\":$p,\"quantity\":$q}"
done

curl -X POST http://localhost:8000/api/models/fit \
  -H "Content-Type: application/json" \
  -d '{"model_type":"linear"}'

curl -X POST http://localhost:8000/api/optimize \
  -H "Content-Type: application/json" \
  -d '{"unit_cost":30,"objective":"profit"}'

## Тесты

pytest tests/ -v

## Лицензия
MIT
