PRAGMA foreign_keys = ON;

-- USERS TABLE
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0,
    is_equipment_manager BOOLEAN NOT NULL DEFAULT 0
);

-- EQUIPMENT TYPES
CREATE TABLE IF NOT EXISTS equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- INDIVIDUAL EQUIPMENT ITEMS
CREATE TABLE IF NOT EXISTS equipment_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id INTEGER NOT NULL,

    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE
);

-- RESERVATIONS
CREATE TABLE IF NOT EXISTS reservation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reservation_date TEXT,
    created_date TEXT,
    approved_date TEXT,
    returned_date TEXT,
    rented_date TEXT,

    order_number INTEGER DEFAULT 0,

    customer_id INTEGER,
    approver_id INTEGER,

    approved BOOLEAN NOT NULL DEFAULT 0,
    cancelled BOOLEAN NOT NULL DEFAULT 0,

    FOREIGN KEY (customer_id) REFERENCES user(id),
    FOREIGN KEY (approver_id) REFERENCES user(id)
);

-- MANY-TO-MANY: reservation × equipment_item
CREATE TABLE IF NOT EXISTS equipment_item_reservation (
    equipment_item_id INTEGER NOT NULL,
    reservation_id INTEGER NOT NULL,

    PRIMARY KEY (equipment_item_id, reservation_id),

    FOREIGN KEY (equipment_item_id) REFERENCES equipment_item(id),
    FOREIGN KEY (reservation_id) REFERENCES reservation(id)
);

-- COMMENTS TABLE
CREATE TABLE IF NOT EXISTS comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    user_id INTEGER NOT NULL,     -- comment author
    equipment_item_id INTEGER,
    reservation_id INTEGER,

    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (equipment_item_id) REFERENCES equipment_item(id),
    FOREIGN KEY (reservation_id) REFERENCES reservation(id)
);
