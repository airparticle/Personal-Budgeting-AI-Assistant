import React, { useMemo, useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  LinearProgress,
  Alert
} from '@mui/material';
import Grid from '@mui/material/Grid';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { dataService } from '../../services/data';

const GoalTracker: React.FC = () => {
  const queryClient = useQueryClient();
  const [error, setError] = useState('');

  const { data: goals = [] } = useQuery({
    queryKey: ['goals'],
    queryFn: dataService.getGoals
  });

  const initialGoal = { goal_name: '', target_value: '', current_progress: '' };
  const [goalForm, setGoalForm] = useState(initialGoal);

  const createMutation = useMutation({
    mutationFn: (payload: any) => dataService.createGoal({
      goal_name: payload.goal_name,
      target_value: parseFloat(payload.target_value),
      current_progress: parseFloat(payload.current_progress || '0')
    }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['goals'] });
      setGoalForm(initialGoal);
      setError('');
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to create goal');
    }
  });

  const totalTargets = useMemo(
    () => goals.reduce((sum, g) => sum + g.target_value, 0),
    [goals]
  );

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setGoalForm({ ...goalForm, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!goalForm.goal_name || !goalForm.target_value) {
      setError('Goal name and target value are required.');
      return;
    }
    createMutation.mutate(goalForm);
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>Goal Tracker</Typography>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {createMutation.isSuccess && <Alert severity="success" sx={{ mb: 2 }}>Goal added!</Alert>}

      <Box component="form" onSubmit={handleSubmit} sx={{ mb: 3 }}>
        <Grid container spacing={2}>
          <Grid size={{ xs: 12, md: 6 }}>
            <TextField
              required
              fullWidth
              label="Goal Name"
              name="goal_name"
              value={goalForm.goal_name}
              onChange={handleChange}
              placeholder="e.g. Emergency Fund"
            />
          </Grid>
          <Grid size={{ xs: 12, md: 3 }}>
            <TextField
              required
              fullWidth
              label="Target ($)"
              name="target_value"
              type="number"
              inputProps={{ step: '0.01' }}
              value={goalForm.target_value}
              onChange={handleChange}
            />
          </Grid>
          <Grid size={{ xs: 12, md: 3 }}>
            <TextField
              fullWidth
              label="Current ($)"
              name="current_progress"
              type="number"
              inputProps={{ step: '0.01' }}
              value={goalForm.current_progress}
              onChange={handleChange}
            />
          </Grid>
          <Grid size={{ xs: 12 }}>
            <Button
              type="submit"
              variant="contained"
              fullWidth
              disabled={createMutation.isPending}
            >
              {createMutation.isPending ? 'Adding...' : 'Add Goal'}
            </Button>
          </Grid>
        </Grid>
      </Box>

      <Typography variant="subtitle2" color="textSecondary" sx={{ mb: 1 }}>
        Total targets: ${totalTargets.toFixed(2)}
      </Typography>

      {goals.length === 0 && (
        <Typography variant="body2" color="textSecondary">
          No goals yet. Add one to start tracking progress.
        </Typography>
      )}

      <Box sx={{ display: 'grid', gap: 2 }}>
        {goals.map((g) => {
          const pct = g.target_value > 0
            ? Math.min(100, (g.current_progress / g.target_value) * 100)
            : 0;

          return (
            <Paper key={g.goal_id} sx={{ p: 2 }} variant="outlined">
              <Typography variant="subtitle1">{g.goal_name}</Typography>
              <Typography variant="body2" color="textSecondary">
                ${g.current_progress.toFixed(2)} / ${g.target_value.toFixed(2)} ({pct.toFixed(0)}%)
              </Typography>
              <LinearProgress variant="determinate" value={pct} sx={{ mt: 1 }} />
            </Paper>
          );
        })}
      </Box>
    </Paper>
  );
};

export default GoalTracker;