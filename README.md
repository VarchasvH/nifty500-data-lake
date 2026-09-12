# Nifty 500 Data Lake

An automated, end-to-end AWS data lake that ingests daily stock price data 
for all 500 Nifty 500 constituents, transforms it, and serves it for analytics.

## Architecture

![Architecture Diagram](architecture.png)

Nifty 500 ticker metadata stored in S3 is used by an AWS Lambda function 
to fetch daily OHLCV price data from the NSE via yfinance. The raw data 
lands in S3 as Parquet files partitioned by year and month. AWS Glue reads 
the raw layer, applies transformations, and writes cleaned data to a separate 
S3 transformed bucket. The transformed data is then loaded into Amazon 
Redshift using the COPY command, leveraging Redshift's MPP architecture for 
fast analytical queries. A QuickSight dashboard sits on top for visualization.

## Pipeline Flow
```
S3 Raw (metadata/tickers)
↓ (EventBridge daily trigger)
AWS Lambda (yfinance API → S3 Raw/stocks/)
↓ (Parquet, partitioned by year/month)
AWS Glue PySpark Job (S3 Raw → S3 Transformed)
↓ (cleaned, enriched Parquet)
Amazon Redshift (COPY from S3)
↓ (MPP serving layer)
Amazon QuickSight Dashboard
```

## Tech Stack

**AWS Services:**
- Amazon S3 — raw and transformed data lake layers
- AWS Lambda — serverless daily ingestion
- Amazon EventBridge — scheduled trigger
- AWS Glue — PySpark transformation
- Amazon Redshift Serverless — analytical serving layer
- Amazon QuickSight — visualization

**Python Libraries:**
- yfinance — NSE stock data ingestion
- pandas — data manipulation
- awswrangler — S3/Redshift integration
- pyarrow — Parquet serialization
- boto3 — AWS SDK

## Data

- **Source:** NSE via yfinance API
- **Coverage:** 500 Nifty 500 constituent stocks
- **History:** 2016 – present
- **Grain:** Daily OHLCV (Open, High, Low, Close, Volume)
- **Format:** Parquet, partitioned by year/month

## Dashboard

QuickSight dashboard showing:
- Nifty 500 index trend (2016–present)
- Top gainers and losers
- 52-week highs and lows
- Sector-wise performance

## Demo

[Video walkthrough](link-to-video)
