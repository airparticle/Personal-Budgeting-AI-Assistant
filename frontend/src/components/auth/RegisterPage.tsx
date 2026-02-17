import React, { useState } from 'react';
import { Container, Paper, TextField, Button, Typography, Box, Alert, Link } from '@mui/material';
import { AccountBalance } from '@mui/icons-material';
import { authService } from '../../services/auth';

const RegisterPage: React.FC = () => {
  const [formData, setFormData] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await authService.register(formData);
      setSuccess(true);
      setTimeout(() => window.location.href = '/login', 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Paper elevation={3} sx={{ padding: 4, width: '100%' }}>
          <Typography component="h1" variant="h5" align="center">Sign Up</Typography>
          {error && <Alert severity="error" sx={{ my: 2 }}>{error}</Alert>}
          {success && <Alert severity="success" sx={{ my: 2 }}>Success! Redirecting...</Alert>}
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1 }}>
            <TextField margin="normal" required fullWidth label="Username"
              onChange={(e) => setFormData({...formData, username: e.target.value})} />
            <TextField margin="normal" required fullWidth label="Email"
              onChange={(e) => setFormData({...formData, email: e.target.value})} />
            <TextField margin="normal" required fullWidth label="Password" type="password"
              onChange={(e) => setFormData({...formData, password: e.target.value})} />
            <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>Register</Button>
            <Link href="/login" variant="body2">Already have an account? Sign In</Link>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default RegisterPage;