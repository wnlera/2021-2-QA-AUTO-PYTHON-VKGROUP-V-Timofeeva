import pandas as pd
from model import RequestCount, CountWithTypes, FrequentRequests, ClientErrorRequests, ServerErrorRequests


class StatsORM:

    def __init__(self, client):
        self.client = client
        self.log_file = open(r"C:\Users\Valery\Downloads\access.log", "r")
        self.df = pd.read_csv(self.log_file,
                              sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
                              engine='python',
                              usecols=[0, 3, 4, 5, 6, 7, 8],
                              names=['ip', 'time', 'request', 'status', 'size', 'referer', 'user_agent'],
                              na_values='-',
                              header=None,
                              )
        self.df["method"], self.df["url"] = StatsORM.request_split(self.df['request'].values)

    @staticmethod
    def trim(seq, limit):
        return seq[:min(limit, len(seq))]

    @staticmethod
    def request_split(input_string_vec):
        methods = []
        urls = []
        for elem in input_string_vec:
            result = elem[1:-1].split(" ")
            methods.append(StatsORM.trim(result[0], 8))
            urls.append(StatsORM.trim(result[1], 80))
        return [methods, urls]

    def get_requests_count(self):
        numbers = self.df.shape[0]
        request_count = RequestCount(count=numbers)
        self.client.session.add(request_count)
        self.client.session.commit()
        return request_count

    def get_requests_type_count(self):
        df = self.df.method.value_counts().to_frame().reset_index()
        df.columns = ["method", "count"]
        for row in df.iterrows():
            row = row[1]
            entry = CountWithTypes(method=row["method"], count=row["count"])
            self.client.session.add(entry)
        self.client.session.commit()

    def get_frequent_requests(self, top=10):
        df = self.df.url.value_counts().nlargest(top).reset_index()
        df.columns = ["url", "count"]
        for row in df.iterrows():
            row = row[1]
            entry = FrequentRequests(url=row["url"], count=row["count"])
            self.client.session.add(entry)
        self.client.session.commit()

    def get_biggest_client_error_requests(self, top=5):
        df = self.df[self.df.status // 100 == 4].nlargest(top, "size").loc[:, ["url", "status", "size", "ip"]]
        for row in df.iterrows():
            row = row[1]
            entry = ClientErrorRequests(url=row["url"],
                                        status=row["status"],
                                        size=row["size"],
                                        ip=row["ip"])
            self.client.session.add(entry)
        self.client.session.commit()

    def get_frequent_server_error_requests(self, top=5):
        df = self.df[self.df.status // 100 == 5].ip.value_counts().nlargest(top).reset_index()
        df.columns = ["ip", "count"]
        for row in df.iterrows():
            row = row[1]
            entry = ServerErrorRequests(ip=row["ip"],
                                        count=row["count"])
            self.client.session.add(entry)
        self.client.session.commit()
