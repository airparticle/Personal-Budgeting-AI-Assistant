import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { dataService } from '../../services/data';
import TransactionForm from '../transactions/TransactionForm';
import SpendingChart from '../analytics/SpendingChart';
import GoalTracker from '../goals/GoalTracker';

const Dashboard: React.FC = () => {
  const { data: transactions = [] } = useQuery({
    queryKey: ['transactions'],
    queryFn: dataService.getTransactions
  });

  const { data: prediction } = useQuery({
    queryKey: ['prediction'],
    queryFn: dataService.getSpendingPrediction
  });

  const totalSpent = transactions.reduce((sum, t) => sum + t.amount, 0);

  return (
    <>
      <div className="dashboard-container">
        <h1>Financial Insights</h1>
        <div className="dashboard-grid" style={{ display: 'flex', gap: '20px' }}>
          <section className="chart-section" style={{ flex: 1 }}>
            <SpendingChart />
          </section>

          <section className="actions-section" style={{ flex: 1 }}>
            <h3>Add Transaction</h3>
            <TransactionForm />
          </section>
        </div>
      </div>

      <Box sx={{ flexGrow: 1, mt: 4 }}>
        <Grid container spacing={3}>
          {/* Stats Cards */}
          {/* FIX: Use 'size' prop for Grid v2 */}
          <Grid size={{ xs: 12, sm: 6, md: 4 }}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" color="textSecondary">Total Spent</Typography>
              <Typography variant="h4">${totalSpent.toFixed(2)}</Typography>
            </Paper>
          </Grid>

          <Grid size={{ xs: 12, sm: 6, md: 4 }}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" color="textSecondary">Transactions</Typography>
              <Typography variant="h4">{transactions.length}</Typography>
            </Paper>
          </Grid>

          <Grid size={{ xs: 12, sm: 6, md: 4 }}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" color="textSecondary">AI Prediction</Typography>
              <Typography variant="h4">${prediction?.predicted_amount?.toFixed(2) || '0.00'}</Typography>
              <Typography variant="body2" color="textSecondary">
                Confidence: {(prediction?.confidence_score ?? 0).toFixed(2)}
              </Typography>
              {prediction?.message && (
                <Typography variant="body2" color="textSecondary">
                  {prediction.message}
                </Typography>
              )}
            </Paper>
          </Grid>

          <Grid size={{ xs: 12 }}>
            <GoalTracker />
          </Grid>

          {/* Welcome Message */}
          <Grid size={{ xs: 12 }}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>Welcome to your Finance AI Assistant! 🎉</Typography>
              <Typography variant="body1">
                Your backend is successfully connected. Start by adding some transactions to see AI predictions and insights.
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </>
  );
};

export default Dashboard;