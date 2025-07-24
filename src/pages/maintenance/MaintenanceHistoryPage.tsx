import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { History, Refresh } from '@mui/icons-material';

const MaintenanceHistoryPage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Maintenance History
          </Typography>
          <Typography variant="body1" color="textSecondary">
            View past maintenance activities and reports.
          </Typography>
        </Box>
        <Button variant="outlined" startIcon={<Refresh />}>
          Refresh
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <History sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">Maintenance History</Typography>
          </Box>
          <Typography color="textSecondary">
            Maintenance history functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default MaintenanceHistoryPage;