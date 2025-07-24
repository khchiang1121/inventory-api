import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { Schedule, Add } from '@mui/icons-material';

const MaintenanceSchedulePage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Maintenance Schedule
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Schedule and manage maintenance windows.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<Add />}>
          Schedule Maintenance
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Schedule sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">Maintenance Scheduling</Typography>
          </Box>
          <Typography color="textSecondary">
            Maintenance scheduling functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default MaintenanceSchedulePage;