# 🏦 ATM Banking System

A console-based ATM Banking System developed in Python.

This project simulates common ATM and banking operations such as
secure login, cash withdrawal, deposits, money transfers, transaction
history, account statements, receipts, and administrative management.

---

## 🚀 Features

### 👤 User Features

- Secure account login
- SHA-256 PIN hashing
- Maximum 3 incorrect PIN attempts
- Temporary account lock after failed attempts
- Check account balance
- Cash withdrawal
- Cash deposit
- Money transfer between accounts
- Daily withdrawal limit
- Change PIN
- Transaction history
- Transaction filtering
- Unique Transaction IDs
- Account statement
- CSV statement export
- Transaction receipt generation
- Persistent account data using JSON

---

## 🔐 Security Features

- PINs are stored using SHA-256 hashing
- PIN is hidden while entering using `getpass`
- Account locks after 3 incorrect PIN attempts
- Temporary lock duration of 60 seconds
- PIN cannot be changed to the same old PIN
- Input validation for banking operations

---

## 👨‍💼 Admin Panel

The project also includes an administrative panel.

### Admin Features

- Admin login
- Dashboard
- View all accounts
- Search accounts
- Unlock locked accounts
- Create new accounts
- Delete accounts
- View all transactions
- View account transaction history
- Transaction search and filtering
- Monitor transaction amounts

### Demo Admin Credentials

```text
Admin ID: admin
Admin Password: admin123