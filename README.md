Тема проекта -- Анализ рынка недвижимости США. Автор -- Владимир Солуянов.
Основной датасет -- realtor-data.csv.
Мой проект состоит из двух частей:
1. Общий анализ рынка недвижимости США. Файл -- 1_part.ipynb. По ходу написания кода я прилагал соответствующую документацию, поэтому здесь подробно его описывать не буду.
2. Анализ геоданных на Streamlit. Файл --  map_app(2_part).py. В этой части я использовал второй датасет (zips.txt) для получения точных географических данных. Карта map.html
прикреплена на случай, если будут проблемы с запуском стримлита. Далее по критериям пользователя строятся графики c использованием SQLite и выдается картинка по соответствующему 
запросу с помощью API Google. Для построения карты использовались не все данные, в силу большого времени компиляции.
