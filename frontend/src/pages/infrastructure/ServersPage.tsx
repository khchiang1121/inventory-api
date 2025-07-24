import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { Computer, Add } from '@mui/icons-material';

const ServersPage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Physical Servers
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage physical server infrastructure.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<Add />}>
          Add Server
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Computer sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">Server Management</Typography>
          </Box>
          <Typography color="textSecondary">
            Physical server management functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ServersPage;