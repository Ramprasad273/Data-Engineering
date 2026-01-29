
-- Raw Transactions Table
CREATE TABLE raw_transactions (
    transaction_id VARCHAR(255) PRIMARY KEY,
    transaction_time TIMESTAMP,
    customer_id VARCHAR(255),
    merchant_id VARCHAR(255),
    transaction_amount DECIMAL(18, 2),
    payment_method VARCHAR(50),
    device_id VARCHAR(255),
    ip_address VARCHAR(50),
    geo_latitude DECIMAL(9, 6),
    geo_longitude DECIMAL(9, 6),
    is_successful BOOLEAN,
    ingestion_date DATE
);

-- Customer Dimension Table
CREATE TABLE dim_customers (
    customer_id VARCHAR(255) PRIMARY KEY,
    kyc_status VARCHAR(50),
    customer_name VARCHAR(255),
    customer_email VARCHAR(255),
    customer_phone VARCHAR(50),
    registration_date DATE
);

-- Merchant Dimension Table
CREATE TABLE dim_merchants (
    merchant_id VARCHAR(255) PRIMARY KEY,
    merchant_name VARCHAR(255),
    merchant_category VARCHAR(100),
    is_compliant BOOLEAN
);

-- Settlement Fact Table
CREATE TABLE fact_settlements (
    settlement_id VARCHAR(255) PRIMARY KEY,
    transaction_id VARCHAR(255) REFERENCES raw_transactions(transaction_id),
    settlement_date DATE,
    settlement_amount DECIMAL(18, 2),
    is_reconciled BOOLEAN,
    mismatch_reason VARCHAR(255)
);

-- Fraud Features Table
CREATE TABLE fraud_features (
    feature_id VARCHAR(255) PRIMARY KEY,
    customer_id VARCHAR(255),
    merchant_id VARCHAR(255),
    feature_name VARCHAR(100),
    feature_value FLOAT,
    feature_generation_time TIMESTAMP
);

-- Risk Scores Table
CREATE TABLE risk_scores (
    score_id VARCHAR(255) PRIMARY KEY,
    entity_id VARCHAR(255), -- Can be customer_id or merchant_id
    entity_type VARCHAR(50), -- 'customer' or 'merchant'
    risk_score FLOAT,
    score_generation_time TIMESTAMP,
    ml_model_version VARCHAR(50)
);
