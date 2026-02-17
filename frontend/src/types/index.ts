export interface User {
  user_id: number;
  email: string;
  username: string;
  created_at: string;
}

export interface Transaction {
  transaction_id: number;
  user_id: number;
  amount: number;
  category: string;
  description: string;
  timestamp: string;
}

export interface Goal {
  goal_id: number;
  user_id: number;
  goal_name: string;
  target_value: number;
  current_progress: number;
}

export interface SpendingPrediction {
  predicted_amount: number;
  confidence_score: number;
  currency: string;
  message?: string;
}

export interface CategoryBreakdown {
  category: string;
  total_amount: number;
}

export interface LoginForm {
  username: string;
  password: string;
}

export interface RegisterForm {
  username: string;
  email: string;
  password: string;
}