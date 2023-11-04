DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS payments;

-- Create the customers table
CREATE TABLE customers (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  phone VARCHAR(20)
);

-- Create the vehicles table
CREATE TABLE vehicles (
  vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
  price INT,
  model VARCHAR(50)
);

-- Create the bookings table
CREATE TABLE bookings (
  booking_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT,
  vehicle_id INT,
  price INT,
  booking_date DATE,
  start_date DATE,
  end_date DATE,
  FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
  FOREIGN KEY (vehicle_id) REFERENCES vehicles (vehicle_id)
);
