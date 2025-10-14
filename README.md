
# check_debts_web

Веб-интерфейс Django для просмотра должников, карточек арендаторов и PDF-писем.

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata debts/fixtures/sample_data.json
python manage.py runserver
```
Открой http://127.0.0.1:8000/

- Главная — список должников.
- Клик по должнику — карточка с договором, платежами и письмами.
- Клик по письму — откроется PDF на отдельной странице (PDF создается автоматически при первом открытии).
