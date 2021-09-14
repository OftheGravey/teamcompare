FROM apache/airflow:2.1.0

RUN pip install --upgrade pip && \
    pip install riotwatcher &&  \
    pip install selenium