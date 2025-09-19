-- Drop existing tables if needed (for fresh dev setup)
DROP TABLE IF EXISTS status_log;
DROP TABLE IF EXISTS complaints;
DROP TABLE IF EXISTS departments;

-- ===========================
-- Complaints Table
-- ===========================
CREATE TABLE complaints (
    complaint_id VARCHAR(50) PRIMARY KEY,
    user_input   VARCHAR(500) NOT NULL,
    category     VARCHAR(50) NOT NULL,
    subcategory  VARCHAR(50) NOT NULL,
    urgency      VARCHAR(10) NOT NULL,
    status       VARCHAR(20) DEFAULT 'Pending',
    assigned_to  VARCHAR(100),
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ===========================
-- Departments Table
-- ===========================
CREATE TABLE departments (
    dept_id      INT AUTO_INCREMENT PRIMARY KEY,
    category     VARCHAR(50) NOT NULL,
    subcategory  VARCHAR(50) NOT NULL,
    level1_email VARCHAR(100),
    level2_email VARCHAR(100),
    level3_email VARCHAR(100),
    CONSTRAINT uq_category_subcategory UNIQUE (category, subcategory)
);

-- ===========================
-- Status Log Table
-- ===========================
CREATE TABLE status_log (
    log_id       INT AUTO_INCREMENT PRIMARY KEY,
    complaint_id VARCHAR(50) NOT NULL,
    status       VARCHAR(20) NOT NULL,
    assigned_to  VARCHAR(100),
    timestamp    DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_status_complaint FOREIGN KEY (complaint_id)
        REFERENCES complaints (complaint_id)
        ON DELETE CASCADE
);