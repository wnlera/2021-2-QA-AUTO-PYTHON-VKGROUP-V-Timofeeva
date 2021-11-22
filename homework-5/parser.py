import pandas as pd
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-j", "--json", action="store_true", help="save output to json")
args = parser.parse_args()

log_file = open(r"C:\Users\Valery\Downloads\access.log", "r")

df = pd.read_csv(log_file,
                 sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
                 engine='python',
                 usecols=[0, 3, 4, 5, 6, 7, 8],
                 names=['ip', 'time', 'request', 'status', 'size', 'referer', 'user_agent'],
                 na_values='-',
                 header=None,
                 )


def trim(seq, limit=8):
    return seq[:min(limit, len(seq))]


def request_split(input_string_vec):
    methods = []
    urls = []
    for elem in input_string_vec:
        result = elem[1:-1].split(" ")
        methods.append(trim(result[0]))
        urls.append(trim(result[1], 80))
    return [methods, urls]


df["method"], df["url"] = request_split(df['request'].values)

f = open("data.txt", 'w', encoding="utf-8")

print("Общее количество запросов", df.shape[0], sep="\n", file=f)
print(file=f)
print("Общее количество запросов по типу", df.method.value_counts(), sep="\n", file=f)
print(file=f)
print("Топ 10 самых частых запросов", df.url.value_counts().nlargest(10), sep="\n", file=f)
print(file=f)
print("Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой",
      df[df.status // 100 == 4].nlargest(5, "size").loc[:, ["url", "status", "size", "ip"]], sep="\n", file=f)
print(file=f)
print("Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой",
      df[df.status // 100 == 5].ip.value_counts().nlargest(5), sep="\n", file=f)
f.close()


def create_json():
    data = {'tasks': []}
    data['tasks'].append({
        'name': "Общее количество запросов",
        'result': df.shape[0]
    })
    data['tasks'].append({
        'name': "Общее количество запросов по типу",
        'result': df["method"].value_counts().to_dict()
    })
    data['tasks'].append({
        'name': "Топ 10 самых частых запросов",
        'result': df["url"].value_counts().nlargest(10).to_dict()
    })
    data['tasks'].append({
        'name': "Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой",
        'result': df[df["status"] // 100 == 4].nlargest(5, "size").loc[:, ["url", "status", "size", "ip"]].to_dict(
            "index")
    })
    data['tasks'].append({
        'name': "Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой",
        'result': df[df["status"] // 100 == 5].ip.value_counts().nlargest(5).to_dict()
    })

    with open('data.json', 'w', encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)


if args.json:
    create_json()

# g369 - попытка эксплуатировать RCE, хочет положить в корень файлик .php со строкой <?php @evаl($_POST['g369g'])
# чтобы вызывать eval у произвольного текста, отправленного с параметром $_POST
