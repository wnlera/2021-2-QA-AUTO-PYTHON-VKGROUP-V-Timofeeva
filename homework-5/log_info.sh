#!/bin/bash
echo "Смотрим логи..."
echo "Общее количество запросов (1 балл)" > result.txt && grep -c "." access.log >> result.txt

echo -e "\nОбщее количество запросов по типу, например: GET - 20, POST - 10 и т.д." >> result.txt && \
awk '{print $6}' access.log | cut -c2- | sort | uniq -c | sort -rn >> result.txt

echo -e "\nТоп 10 самых частых запросов" >> result.txt && \
awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -n 10 >> result.txt

echo -e "\nТоп 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой" >> result.txt && \
awk '($9 ~ /4[0-9]{2}/)' access.log | awk '{print $1, $7, $9, $10}' | sort -k 4 -rn | head -n 5 >> result.txt

echo -e "\nТоп 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой" >> result.txt && \
awk '($9 ~ /5[0-9]{2}/)' access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -n 5 >> result.txt

echo "Результат в файле ./result.txt"