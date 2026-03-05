# Personal Budgeting AI Assistant 

An intelligent personal finance management application that helps users track spending, set financial goals, and leverage AI for deeper insights into their financial habits.

## Features

- **Transaction Management**: Easily track income and expenses.
- **Goal Tracking**: Set and monitor financial milestones with the `GoalTracker` component.
- **Visual Analytics**: Interactive spending charts and data visualization.
- **AI-Powered Insights**: Backend ML services to analyze spending patterns.
- **Secure Authentication**: User management and protected data access.

## Project Structure

The project is split into two main parts:

- **/backend**: FastAPI application powered by Python 3.12.
  - `app/api`: RESTful API endpoints.
  - `app/ml`: Machine learning models and logic.
  - `app/crud`: Data access layer (Users, Transactions, Goals).
  - `app/models` & `app/schemas`: SQLAlchemy models and Pydantic schemas.
- **/frontend**: Modern React application with TypeScript.
  - `src/components`: UI components including Analytics and Dashboard.
  - `src/services`: Integration with the backend API.
  - `src/hooks`: Custom React hooks for state management.

##  Getting Started

### Prerequisites

- Python 3.12+
- Node.js & npm
- virtualenv

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   # Windows
   .\env\Scripts\activate
   # macOS/Linux
   source env/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your environment variables in a `.env` file.
5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic, Scikit-learn/TensorFlow (ML).
- **Frontend**: React, TypeScript, Chart.js/Recharts.
- **Database**: (e.g., PostgreSQL/SQLite - adjust as needed).

## 📝 License

This project is licensed under the MIT License.
