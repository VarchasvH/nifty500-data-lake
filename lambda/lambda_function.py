# Import the libraries
import boto3 as b3
import pandas as pd
import yfinance as yf
import datetime as dt
import awswrangler as wr
import os

# Environment variables
BUCKET_NAME = os.environ.get('BUCKET_NAME_RAW')
TICKERS_KEY = os.environ.get('TICKERS_KEY')
OUTPUT_PATH = os.environ.get('OUTPUT_PATH_STOCKS')

def get_tickers():
    """
    Function to get the tickers from the s3 bucket
    """
    try:
        s3 = b3.client('s3')
        file_path = s3.get_object(Bucket=BUCKET_NAME, Key=TICKERS_KEY)
        raw_df = pd.read_csv(filepath_or_buffer=file_path['Body'])
        tickers = raw_df['Symbol'].tolist()
        tickers = [stock + '.NS' for stock in tickers]
        return tickers
    except Exception as e:
      print(f"Error fetching tickers from S3: {e}")
      raise


def download_data(tickers):
    """
    Function to download the data from yfinance
    """
    try:
      data = yf.download(tickers, start='2016-01-01', end= dt.datetime.today().strftime('%Y-%m-%d'))
      return data
    except Exception as e:
      print(f"Error downloading data from yfinance: {e}")
      raise

def transform_date(data):
    """
    Function to flatten and transform the date column
    """
    try:
      df = data.stack(future_stack=True).reset_index()
      df['Month'] = df['Date'].dt.month
      df['Year'] = df['Date'].dt.year
      return df
    except Exception as e:
      print(f"Error transforming data: {e}")
      raise

def write_to_s3(df):
    """
    Function to write the data to s3
    """
    try:
      wr.s3.to_parquet(
              df=df,
              path=OUTPUT_PATH,
              dataset=True,
              partition_cols=['Year', 'Month']
          )
    except Exception as e:
      print(f"Error writing data to S3: {e}")
      raise


def lambda_handler(event, context):
    """
    Lambda handler function
    """
    try:
        tickers = get_tickers()
        data = download_data(tickers)
        df = transform_date(data)
        write_to_s3(df)
        return {'statusCode': 200, 'body': 'Ingestion complete'}
    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        return {'statusCode': 500, 'body': 'Ingestion failed'}
