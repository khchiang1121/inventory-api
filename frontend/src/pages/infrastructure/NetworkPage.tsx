import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { NetworkCheck, Add } from '@mui/icons-material';

const NetworkPage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Network
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage network infrastructure and configurations.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<Add />}>
          Add Network
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <NetworkCheck sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">Network Management</Typography>
          </Box>
          <Typography color="textSecondary">
            Network management functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default NetworkPage;