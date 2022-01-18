Веб сервер, позволяющий получать информацию о погоде в выбранном городе.

![image](https://user-images.githubusercontent.com/61735653/149934891-4d7cfd98-1f1d-49ab-b91c-60398771c90f.png)
-> Стартовая страница

![image](https://user-images.githubusercontent.com/61735653/149934999-8de986b0-4533-4ec0-9aac-85ff3cfd54fa.png)
-> Пример страницы ответа

![image](https://user-images.githubusercontent.com/61735653/149935050-ff9e9eda-6694-4550-bafb-fc07b1e69db4.png)
-> Анимация заднего фона зависит от погоды в городе

Сборка в докере: docker-compose up -d --build

Удаление: docker-compose down -v

Ссылка: https://api.openweathermap.org/data/2.5/weather?q=moscow&appid=*YOUR_API_KEY*&units=metric

POST запрос: curl -d '{"source":"openweathermap", "city":"moscow", "temp":2.04, "timezone":10800, "lon":37.6156, "lat":55.7522, "request":"http://localhost:8000/api/moscow"}' -H "Content-Type: application/json" -X POST http://localhost:8000/db
