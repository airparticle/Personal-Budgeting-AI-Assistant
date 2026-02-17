import api from './api';
import { Transaction, Goal, SpendingPrediction, CategoryBreakdown } from '../types';

export const dataService = {
  // Transactions
  async getTransactions(): Promise<Transaction[]> {
    const response = await api.get('/transactions/');
    return response.data;
  },

  async createTransaction(transaction: Omit<Transaction, 'transaction_id' | 'user_id'>) {
    const response = await api.post('/transactions/', transaction);
    return response.data;
  },

  async deleteTransaction(id: number) {
    await api.delete(`/transactions/${id}`);
  },

  // Goals
  async getGoals(): Promise<Goal[]> {
    const response = await api.get('/goals/');
    return response.data;
  },

  async createGoal(goal: Omit<Goal, 'goal_id' | 'user_id'>) {
    const response = await api.post('/goals/', goal);
    return response.data;
  },

  async updateGoal(id: number, goal: Partial<Goal>) {
    const response = await api.put(`/goals/${id}`, goal);
    return response.data;
  },

  async deleteGoal(id: number) {
    await api.delete(`/goals/${id}`);
  },

  // Analytics
  async getSpendingPrediction(): Promise<SpendingPrediction> {
    const response = await api.get('/analytics/prediction');
    return response.data;
  },

  async getCategoryBreakdown(): Promise<CategoryBreakdown[]> {
    const response = await api.get('/analytics/breakdown');
    return response.data;
  }
};