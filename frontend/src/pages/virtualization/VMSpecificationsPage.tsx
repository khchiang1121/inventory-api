import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { Settings, Add } from '@mui/icons-material';

const VMSpecificationsPage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            VM Specifications
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage virtual machine specification templates.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<Add />}>
          Add Specification
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Settings sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">VM Specifications Management</Typography>
          </Box>
          <Typography color="textSecondary">
            VM specifications management functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default VMSpecificationsPage;