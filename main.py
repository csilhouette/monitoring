import requests
import pandas as pd
from dataclasses import dataclass
from fire import Fire
import boto3

if __name__ == '__main__':

    # 1) 4 versions du fichier et 4 compute puis envois dans prometheus
    # 2) Faire un makefile : lance le prometheus, le gateway,
    # lancer le script qui va populate le prometheus a travers la gateway


    data = '# TYPE total_count counter total_count{layer="raw", source="business_events", table="delivery_canceled"} 20'

    response = requests.post('http://localhost:9091/metrics/job/datalake/', data=data)


    @dataclass()
    class Metric:

        name: str
        value: int

    class Loader:

        def load(self, path_to_s3: str) -> pd.DataFrame:
            pass

    class ComputeMetrics:

        def compute(self, df: pd.DataFrame) -> Metric:
            return Metric(name='total_count', value=df.count())

    class PrometheusClient:

        def __init__(self):
            self.prometheus_client = None

        def send_metric(self, metric: Metric):
            pass


    def main(path_to_s3: str, metric_table: str):
        """
        My doc
        """
        loader = Loader()
        compute_metrics = ComputeMetrics()

        df = loader.load(path_to_s3)
        metric = compute_metrics.compute(df)
        PrometheusClient.send_metric(metric)

    if __name__ == '__main__':
        Fire(main)
