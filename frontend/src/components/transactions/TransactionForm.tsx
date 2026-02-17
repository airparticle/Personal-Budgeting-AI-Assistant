import React, { useState } from 'react';
import {
  Paper,
  Box,
  TextField,
  Button,
  Typography,
  MenuItem,
  Alert
} from '@mui/material';
import Grid from '@mui/material/Grid';
import { AddCircleOutline } from '@mui/icons-material';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { dataService } from '../../services/data';

const CATEGORIES = [
  'Housing',
  'Food',
  'Transportation',
  'Utilities',
  'Insurance',
  'Healthcare',
  'Saving',
  'Personal',
  'Entertainment',
  'Miscellaneous'
];

export const TransactionForm: React.FC = () => {
  const queryClient = useQueryClient();
  const [error, setError] = useState('');

  // Initial form state
  const initialFormState = {
    amount: '',
    category: '',
    description: '',
    date: new Date().toISOString().split('T')[0] // Default to today
  };

  const [formData, setFormData] = useState(initialFormState);

  // Mutation to create transaction
  const mutation = useMutation({
    mutationFn: (newTransaction: any) => dataService.createTransaction({
      ...newTransaction,
      amount: parseFloat(newTransaction.amount), // Ensure amount is a number
      timestamp: new Date(newTransaction.date).toISOString() // Format for backend
    }),
    onSuccess: () => {
      // Invalidate 'transactions' query to trigger a refetch in Dashboard
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      // Reset form
      setFormData(initialFormState);
      setError('');
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to add transaction');
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.amount || !formData.category) {
      setError('Amount and Category are required');
      return;
    }
    mutation.mutate(formData);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <AddCircleOutline color="primary" />
        Add Transaction
      </Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {mutation.isSuccess && <Alert severity="success" sx={{ mb: 2 }}>Transaction added!</Alert>}

      <Box component="form" onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          {/* Amount Input */}
          <Grid size={{ xs: 12, sm: 6 }}>
            <TextField
              required
              fullWidth
              label="Amount ($)"
              name="amount"
              type="number"
              inputProps={{ step: "0.01" }}
              value={formData.amount}
              onChange={handleChange}
            />
          </Grid>

          {/* Category Select */}
          <Grid size={{ xs: 12, sm: 6 }}>
            <TextField
              select
              required
              fullWidth
              label="Category"
              name="category"
              value={formData.category}
              onChange={handleChange}
            >
              {CATEGORIES.map((option) => (
                <MenuItem key={option} value={option}>
                  {option}
                </MenuItem>
              ))}
            </TextField>
          </Grid>

          {/* Description Input */}
          <Grid size={{ xs: 12 }}>
            <TextField
              fullWidth
              label="Description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="e.g. Grocery Store, Uber, Rent"
            />
          </Grid>

          {/* Date Input */}
          <Grid size={{ xs: 12 }}>
            <TextField
              required
              fullWidth
              type="date"
              label="Date"
              name="date"
              value={formData.date}
              onChange={handleChange}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>

          <Grid size={{ xs: 12 }}>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={mutation.isPending}
            >
              {mutation.isPending ? 'Adding...' : 'Add Transaction'}
            </Button>
          </Grid>
        </Grid>
      </Box>
    </Paper>
  );
};

export default TransactionForm;