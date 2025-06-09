git add README.md
git add requirements.txt
git add pyproject.toml
git commit -m "دمج تعارضات main مع الملفات المحلية"

# Cashier App

A modern point-of-sale (POS) system built with Python, featuring a user-friendly interface and comprehensive sales management capabilities.

## Features

- User authentication and authorization
- Product management
- Sales tracking and reporting
- Inventory management
- Customer management
- Receipt generation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cashier_app.git
cd cashier_app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Initialize the database:
```bash
python init_db.py
```

2. Run the application:
```bash
python main.py
```

## Project Structure

```
cashier_app/
├── config/         # Configuration files
├── controllers/    # Business logic
├── database/       # Database models and migrations
├── models/         # Data models
├── resources/      # Static resources
├── tests/          # Test files
├── ui/            # User interface components
├── utils/         # Utility functions
└── views/         # View templates
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.