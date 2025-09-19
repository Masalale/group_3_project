-- USERS TABLE
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) UNIQUE,
    is_business BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TRANSACTION_CATEGORIES TABLE  
CREATE TABLE transaction_categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- TRANSACTIONS TABLE
CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    sms_date BIGINT NOT NULL,
    message_body TEXT NOT NULL,
    service_center VARCHAR(20),
    category_id INT NOT NULL,
    amount DECIMAL(15,2),
    fee DECIMAL(10,2) DEFAULT 0,
    new_balance DECIMAL(15,2),
    counterparty_user_id INT,
    direction ENUM('INCOMING', 'OUTGOING', 'DEPOSIT', 'WITHDRAWAL', 'PURCHASE') NOT NULL,
    external_tx_id VARCHAR(50),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign Keys
    FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id),
    FOREIGN KEY (counterparty_user_id) REFERENCES users(user_id)
);

-- SYSTEM_LOGS TABLE
CREATE TABLE system_logs (
    log_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    log_level ENUM('INFO', 'WARNING', 'ERROR') NOT NULL,
    log_message TEXT NOT NULL,
    transaction_id BIGINT,
    processing_stage VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign Keys
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);

-- USER_TRANSACTION_STATS
CREATE TABLE user_transaction_stats (
    stats_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    frequency_count INT DEFAULT 0,
    total_amount DECIMAL(15,2) DEFAULT 0,
    last_transaction_date TIMESTAMP,

    -- Foreign Keys
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id),
    UNIQUE KEY unique_user_category (user_id, category_id)
);