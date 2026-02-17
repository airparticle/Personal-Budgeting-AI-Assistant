import React, { useEffect, useMemo, useState } from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { dataService } from '../../services/data';
import { Box, Typography } from '@mui/material';

ChartJS.register(ArcElement, Tooltip, Legend);

const SpendingChart = () => {
  const [chartData, setChartData] = useState<any>(null);
  const [rawData, setRawData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchBreakdown = async () => {
      try {
        const response = await dataService.getCategoryBreakdown();
        setRawData(response);

        const labels = response.map((item: any) => item.category);
        const amounts = response.map((item: any) => item.total_amount);

        setChartData({
          labels: labels,
          datasets: [
            {
              label: 'Spending by Category',
              data: amounts,
              backgroundColor: [
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
              ],
              hoverOffset: 4,
            },
          ],
        });
      } catch (e: any) {
        setError('Unable to load spending breakdown.');
      } finally {
        setLoading(false);
      }
    };

    fetchBreakdown();
  }, []);

  const total = useMemo(
    () => rawData.reduce((sum, i) => sum + i.total_amount, 0),
    [rawData]
  );

  const topCategories = useMemo(() => {
    return [...rawData]
      .sort((a, b) => b.total_amount - a.total_amount)
      .slice(0, 3);
  }, [rawData]);

  if (loading) return <div>Analyzing your spending...</div>;
  if (error) return <div>{error}</div>;
  if (!chartData || rawData.length === 0) return <div>No data available to visualize.</div>;

  return (
    <Box sx={{ maxWidth: 420, margin: '0 auto' }}>
      <Typography variant="h6" gutterBottom>Where your money goes</Typography>
      <Doughnut data={chartData} />
      <Typography variant="subtitle2" color="textSecondary" sx={{ mt: 2 }}>
        Total: ${total.toFixed(2)}
      </Typography>

      <Box sx={{ mt: 1 }}>
        <Typography variant="subtitle2">Top categories</Typography>
        {topCategories.map((c) => (
          <Typography key={c.category} variant="body2" color="textSecondary">
            {c.category}: ${c.total_amount.toFixed(2)}
          </Typography>
        ))}
      </Box>
    </Box>
  );
};

export default SpendingChart;