# 🏦 ATM Banking System

A console-based ATM Banking System developed in Python.

This project simulates common ATM and banking operations such as secure login, cash withdrawal, deposits, money transfers, transaction history, account statements, receipts, and administrative management.

---

## 🚀 Features

### 👤 User Features

- Secure account login
- SHA-256 PIN hashing
- Hidden PIN input using `getpass`
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
- PIN is hidden while entering
- Account locks after 3 incorrect PIN attempts
- Temporary lock duration of 60 seconds
- Failed login attempts are tracked
- PIN cannot be changed to the same old PIN
- Input validation for banking operations

---

## 👨‍💼 Admin Panel

The project also includes an administrative panel for managing accounts and monitoring transactions.

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
These credentials are for demonstration purposes only.
💰 Banking Operations
💸 Withdrawal

Users can withdraw money if:

Amount is greater than zero
Sufficient balance is available
Daily withdrawal limit has not been exceeded
💵 Deposit

Users can deposit a valid positive amount into their account.

🔄 Money Transfer

Users can transfer money to another registered account.

The system automatically creates:

A TRANSFER transaction for the sender
A RECEIVED transaction for the receiver
🧾 Transaction System

Every new transaction receives a unique Transaction ID.

Example:

TXN-20260925172603-6333

Each transaction stores:

Transaction ID
Date and time
Transaction type
Amount
Balance after transaction
Transaction details

Supported transaction types include:

DEPOSIT
WITHDRAW
TRANSFER
RECEIVED
🧾 Receipt System

After a successful withdrawal, deposit, or transfer, the system displays a transaction receipt.

Receipts are automatically saved inside:

receipts/

Each receipt contains:

Account holder
Account number
Transaction ID
Transaction type
Amount
Date and time
Transaction details
Available balance
📊 Account Statement

The system provides a complete account statement containing:

Transaction ID
Date and time
Transaction type
Amount
Balance
Transaction Filters

Users can filter transactions by:

All Transactions
Deposits
Withdrawals
Transfers
Received Money
📁 CSV Statement Export

Users can export their account statement into CSV format.

Generated statements are stored inside:

statements/

Example:

statement_10001.csv

🛠️ Technologies Used
Python
JSON
CSV
SHA-256 Hashing
getpass
datetime
Decimal
os
time
random
📂 Project Structure
ATM-Banking-System/
│
├── data/
│   └── accounts.json
│
├── receipts/
│
├── screenshots/
│
├── statements/
│
├── .gitignore
├── admin.py
├── database.py
├── LICENSE
├── main.py
├── README.md
├── transactions.py
├── users.py
└── utils.py
File Description
File / Folder	Purpose
main.py	Main ATM application and user operations
admin.py	Admin login and account management
database.py	Account data loading and saving
transactions.py	Transaction creation and unique Transaction IDs
users.py	Default account information
utils.py	Receipts, statements, filtering and CSV export
data/	Stores persistent account data
receipts/	Stores generated transaction receipts
statements/	Stores exported CSV statements
screenshots/	Project demonstration screenshots
.gitignore	Prevents unnecessary files from being uploaded
LICENSE	Project license
README.md	Project documentation
▶️ How to Run
Step 1: Clone the Repository
git clone <your-repository-url>
Step 2: Open the Project Folder
cd ATM-Banking-System
Step 3: Run the Program
python3 main.py
👤 Demo User Accounts

The project contains sample accounts for testing.

Account Number: 10001
Account Holder: Nandini
Account Number: 20002
Account Holder: Rahul
Account Number: 30003
Account Holder: Priya

PINs are stored securely as SHA-256 hashes inside the database.

📌 Main ATM Menu
1. Check Balance
2. Withdraw Cash
3. Deposit Cash
4. Transfer Money
5. Transaction History & Filter
6. Export Statement to CSV
7. Change PIN
8. Logout
📌 Admin Menu
1. Dashboard
2. View All Accounts
3. Search Account
4. Unlock Account
5. Create New Account
6. Delete Account
7. View All Transactions
8. Account Transaction History
9. Transaction Search & Filter
10. Logout
🎯 Project Objective

The objective of this project is to simulate a basic banking environment using Python while implementing important programming concepts such as:

File handling
JSON data storage
Authentication
PIN hashing
Exception handling
Functions
Modules
Data validation
Transaction management
Administrative controls
Persistent data storage
🔮 Future Improvements

The project can be further enhanced with:

GUI interface
MySQL database integration
OTP-based authentication
Email/SMS transaction notifications
Advanced admin authentication
Account type management
Interest calculation
ATM cash inventory management
Bank API integration
📸 Screenshots

Screenshots demonstrating the working of the ATM Banking System are available in the screenshots/ folder.

The screenshots demonstrate features such as:

ATM login
Cash deposit
Transaction receipt
Transaction history
Account statement
Transaction filtering
Admin panel
👩‍💻 Author

Nandini Kumari

B.Tech — Robotics & Artificial Intelligence

📄 License

This project is created for educational and portfolio purposes.


