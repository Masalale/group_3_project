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

-- Sample DML statements

-- Insert into transaction_categories
INSERT INTO transaction_categories (category_name, description) VALUES
('MONEY_RECEIVED', 'Incoming money transfers from other users'),
('PAYMENT', 'Payments to merchants or individuals'),
('BANK_DEPOSIT', 'Cash deposits from bank to mobile money'),
('AIRTIME_PURCHASE', 'Mobile airtime and data bundle purchases'),
('CASH_WITHDRAWAL', 'Cash withdrawals through agents'),
('MONEY_TRANSFER', 'Outgoing money transfers to other users'),
('UTILITY_PAYMENT', 'Electricity, water, and other utility payments');

-- Insert into users
INSERT INTO users (full_name, phone_number, is_business) VALUES
('Jane Smith', '250791666013', FALSE),
('Samuel Carter', '250788995464', FALSE),
('Alex Doe', '250790777777', FALSE),
('Robert Brown', '250789888888', FALSE),
('Linda Green', '250788999123', FALSE),
('DIRECT PAYMENT LTD', NULL, TRUE),
('MTN Airtime', NULL, TRUE);

-- Insert into transactions (We used AI to parse data from the XML data)
INSERT INTO transactions (sms_date, message_body, service_center, category_id, amount, fee, new_balance, counterparty_user_id, direction, external_tx_id) VALUES
(1715351458724, 'You have received 2000 RWF from Jane Smith (*********013) on your mobile money account at 2024-05-10 16:30:51. Financial Transaction Id: 76662021700.', '+250788110381', 1, 2000.00, 0.00, 2000.00, 1, 'INCOMING', '76662021700'),
(1715351506754, 'TxId: 73214484437. Your payment of 1,000 RWF to Jane Smith 12845 has been completed at 2024-05-10 16:31:39. Your new balance: 1,000 RWF. Fee was 0 RWF.', '+250788110381', 2, 1000.00, 0.00, 1000.00, 1, 'OUTGOING', '73214484437'),
(1715369560245, 'TxId: 51732411227. Your payment of 600 RWF to Samuel Carter 95464 has been completed at 2024-05-10 21:32:32. Your new balance: 400 RWF. Fee was 0 RWF.', '+250788110381', 2, 600.00, 0.00, 400.00, 2, 'OUTGOING', '51732411227'),
(1715445936412, 'A bank deposit of 40000 RWF has been added to your mobile money account at 2024-05-11 18:43:49. Your NEW BALANCE: 40400 RWF.', '+250788110381', 3, 40000.00, 0.00, 40400.00, NULL, 'DEPOSIT', NULL),
(1715506895734, 'Your payment of 2000 RWF to Airtime with token has been completed at 2024-05-12 11:41:28. Fee was 0 RWF. Your new balance: 25280 RWF.', '+250788110381', 4, 2000.00, 0.00, 25280.00, 7, 'PURCHASE', '13913173274'),
(1715520000000, 'You have received 1500 RWF from Alex Doe on your mobile money account. Your new balance: 26780 RWF.', '+250788110381', 1, 1500.00, 0.00, 26780.00, 3, 'INCOMING', '89012345678'),
(1715530000000, 'Cash withdrawal of 5000 RWF completed at agent location. Your new balance: 21780 RWF. Fee was 100 RWF.', '+250788110381', 5, 5000.00, 100.00, 21780.00, NULL, 'WITHDRAWAL', '45678901234');

-- Insert into system_logs
INSERT INTO system_logs (log_level, log_message, transaction_id) VALUES
('INFO', 'Successfully parsed SMS from M-Money service', 1),
('INFO', 'Transaction categorized as MONEY_RECEIVED', 1),
('WARNING', 'Phone number partially masked in SMS content', 1),
('INFO', 'Payment transaction processed successfully', 2),
('ERROR', 'Failed to extract complete phone number from SMS', 3),
('INFO', 'Bank deposit transaction recorded', 4),
('INFO', 'Airtime purchase transaction completed', 5);

-- Insert into user_transaction_stats
INSERT INTO user_transaction_stats (user_id, category_id, frequency_count, total_amount, last_transaction_date) VALUES
(1, 1, 1, 2000.00, '2024-05-10 16:30:51'),
(1, 2, 2, 1600.00, '2024-05-10 16:31:39'),
(2, 2, 1, 600.00, '2024-05-10 21:32:32'),
(3, 1, 1, 1500.00, '2024-05-12 15:20:00'),
(7, 4, 1, 2000.00, '2024-05-12 11:41:28'),
(1, 3, 0, 0.00, NULL),
(2, 1, 0, 0.00, NULL);