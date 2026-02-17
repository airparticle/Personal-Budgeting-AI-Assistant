import api from './api';
import { LoginForm, RegisterForm, User } from '../types';

export const authService = {
  async login(credentials: LoginForm) {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await api.post('/login/access-token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });

    const { access_token } = response.data;
    localStorage.setItem('access_token', access_token);
    return access_token;
  },

  async register(userData: RegisterForm) {
    const response = await api.post('/users/register', userData);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get('/users/me');
    return response.data;
  },

  logout() {
    localStorage.removeItem('access_token');
  },

  isAuthenticated() {
    return !!localStorage.getItem('access_token');
  }
};