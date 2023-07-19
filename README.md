[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://airlines-customer-satisfaction.streamlit.app/)

# ML-сервис для предсказания удовлетворённости клиентов авиакомпаний

![Header image](https://github.com/dm1trykrylov/Airlines-Customer-satisfaction/blob/main/images/Airline-satisfaction-cover-1-1536x590.png)

## Цель
Этот проект призван на основании реальных результатов опроса клиентов авиакомпании выявить ключевые факторы, влияющие на впечатление клиентов и научиться предсказывать удовлетворённость полётом.

Проект создан в рамках буткемпа ["Разработка ML-сервиса: от идеи к прототипу"](https://www.hse.ru/ma/mlds/mlservice/).

## Этапы проекта:

### Разведочный анализ
Его результаты в файле [`customers.ipynb`](customers.ipynb). [Датасет](datasets/clients.csv), данные из которого были использованы.
* В данных были пропуски. Строки с пропусками и выбросами были исключены из датасета.
* Проанализирована линейная корреляция признаков.
* Построены графики распределения клиентов по классам для категориальных признаков.
* Под графиками приведены некоторые наблюдения.

### Машинное обучение
* Категориальные признаки закодированы с помощью Ordinal Encoder из scikit-learn
* Все признаки масштабированы с использованием MinMaxScaler
* Обучены 3 модели: Logistic Regression, SVM и CatBoost.
* С помощью **Catboost Classifier** получены предсказания, выдающие результат выше 95% по всем использованным метрикам. Это наилучший результат.
* Результат получилось ещё немного улучшить.

### Создание веб-приложения 
Приложение создано с помощью **Streamlit**
* Поддерживаются 2 языка интерфейса - русский и английский.
* В приложении есть анкета. После заполнения можно получить предсказание удовлетворённости.
* Основной файл - [`app.py`](app.py), сначала запускается он. Он отвечает за отрисовку интерфейса и обработку пользовательского ввода.
* В файле [`model.py`](model.py) данные из анкеты подготавливаются так же, как при обучении моделейна датасете
* Для предсказания загружается модель, показавшая наилучший результат - CatBoost.
* В итоге пользователь получает предсказание и вероятности.
