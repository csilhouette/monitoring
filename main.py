import requests
import pandas as pd
from dataclasses import dataclass
import time
from fire import Fire
from config import PATH_TO_FILE

if __name__ == '__main__':

    # 1) 4 versions du fichier et 4 compute puis envois dans prometheus
    # 2) Faire un makefile : lance le prometheus, le gateway,
    # lancer le script qui va populate le prometheus a travers la gateway

    @dataclass()
    class Metric:

        name: str
        type: str
        value: int
        labels: dict

    class Loader:
        @staticmethod
        def load(path: str) -> pd.DataFrame:
            return pd.read_csv(path)


    class ComputeMetrics:
        @staticmethod
        def compute(df: pd.DataFrame, name: str, type: str, labels: dict) -> Metric:
            if name == 'total_count':
                return Metric(name=name, type=type, labels=labels, value=df['first_name'].shape[0])

    def prom_query_factory(metric: Metric):

        return '# TYPE {metric_name} {metric_type}\n{metric_name}{labels} {valeur}\n'.format(
            metric_name=metric.name,
            metric_type=metric.type,
            labels=metric.labels,
            valeur=str(metric.value))

    class PrometheusClient:

        def __init__(self):
            self.prometheus_client = None

        @staticmethod
        def send_metric(metric: Metric):

            data = prom_query_factory(metric)

            response = requests.post('http://localhost:9091/metrics/job/datalake/', data=data)
            print(response)

    def main(path_to_s3: str = None, metric_table: str = None):
        """
        My doc
        """
        for hour in range(19, 24):

            path = PATH_TO_FILE.format(hour)

            df = Loader.load(path=path)

            metric = ComputeMetrics. \
                compute(df,
                        name='total_count',
                        type='gauge',
                        labels="{layer=\"raw\", source=\"business_events\", table=\"delivery_canceled\"}")

            PrometheusClient.send_metric(metric=metric)
            time.sleep(10)


    if __name__ == '__main__':
        main()
        #Fire(main)
