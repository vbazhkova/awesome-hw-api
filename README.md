# awesome-hw-api

Данный апи может использоваться при создании приложений, сайтов связаныых с животными. Например, если добавить дополнительный функционал, то можно его можно использовать:
- в вет.клиниках
- в сервисах по выгулу животных
- в сервисах, где люди берут себе животных на передержку
- в гостиницах для животных и др.

В текущей реализации данный API может использоваться как часть какой-то большой системы. 

В данный момент в API существует следующие доступные ручки:
1) /welcome статический welcome ответ
2) /pets get получаем все животных или животных по id или по type
3) /pets post добавляем нового животного с параметрами type и name
4) /pets delete удаляем животного по id
5) /pets patch изменяем имя животному по id
6) /image/{urlname} получаем картинку животного из object storage
7) /caterror/{status_code} получаем картинку кота с HTTP ошибкой
8) /random/cat получаем JSON с картинкой и размерами c apikey в хедере
