CREATE TABLE device (
        id INTEGER NOT NULL,
        device_ip_addr VARCHAR(255),
        device_protocol VARCHAR(255),
        device_topic VARCHAR(255),
        device_id VARCHAR(255),
        PRIMARY KEY (id),
        UNIQUE (device_id)
);
