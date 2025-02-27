﻿# tatweer-backend
 
A sophisticated FastAPI-based logistics management system with AI-powered decision support, real-time updates via WebSocket, and comprehensive inventory management capabilities.

## 🌟 Features

- **AI-Powered Decision Support**
  - Risk analysis and mitigation recommendations
  - Historical context-based decision making
  - Real-time decision updates via WebSocket

- **Authentication & Security**
  - JWT-based authentication
  - Secure password hashing with bcrypt
  - Role-based access control

- **Inventory Management**
  - Complete CRUD operations
  - Real-time inventory tracking
  - Automated inventory updates

- **Order Processing**
  - Order lifecycle management
  - Order tracking and status updates
  - Historical order data

- **Real-time Updates**
  - WebSocket integration for live updates
  - Decision context notifications
  - System status monitoring
  - **Shipment Management**
  - Complete shipment lifecycle tracking
  - Real-time shipment status updates
  - Automated shipment creation and monitoring

- **Production Planning**
  - Production record management
  - Real-time production tracking
  - Production capacity monitoring

- **S&OP (Sales & Operations Planning)**
  - Automated S&OP plan generation
  - Sales and production data integration
  - Demand forecasting
  - Production capacity analysis

## 🚀 Technology Stack

- **Backend Framework**: FastAPI
- **Database**: MongoDB
- **AI Integration**: OpenRouter API (Google Gemini Pro)
- **Authentication**: JWT + bcrypt
- **Real-time Communication**: WebSocket
- **Documentation**: OpenAPI (Swagger)

## 📋 Prerequisites

- Python 3.8+
- MongoDB
- OpenRouter API key
- Environment variables setup

## ⚙️ Environment Variables

Create a `.env` file in the root directory with the following variables:
OPENROUTER_API_KEY=your_openrouter_api_key
SECRET_KEY=your_jwt_secret_key
MONGODB_URL=your_mongodb_connection_string 


## 🛠️ Installation

1. Clone the repository:
git clone https://github.com/TATWEER-Wizara/backend
cd backend


2. Create and activate virtual environment:
python -m venv venv
# on Mac: source venv/bin/activate
# On Windows: venv\Scripts\activate


3. Install dependencies:
pip install -r requirements.txt


4. Start the server:
uvicorn app.main:app --reload


## 🔌 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Decision Context
- `POST /api/decision-context/submit/` - Submit context for AI analysis
- `POST /api/decision-context/best-decision/` - Get AI-recommended decision
- `GET /api/decision-contexts/user` - Get user's decision history

### Inventory Management
- `POST /inventory` - Create inventory record
- `GET /inventory/{inventory_id}` - Get specific inventory
- `PUT /inventory/{inventory_id}` - Update inventory
- `DELETE /inventory/{inventory_id}` - Delete inventory
- `GET /inventory` - List all inventory

### Order Management
- `POST /orders` - Create order
- `GET /orders/{order_id}` - Get specific order
- `PUT /orders/{order_id}` - Update order
- `DELETE /orders/{order_id}` - Delete order
- `GET /orders` - List all orders

### WebSocket
- `WS /ws` - Real-time updates connection

## 📚 API Documentation

Access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`


## 🔐 Security

- All endpoints (except authentication) require JWT token
- Passwords are hashed using bcrypt
- API keys and sensitive data are managed through environment variables

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request






