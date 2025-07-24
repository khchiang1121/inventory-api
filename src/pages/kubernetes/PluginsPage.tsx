import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { Extension, Add } from '@mui/icons-material';

const PluginsPage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Kubernetes Plugins
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage Kubernetes cluster plugins and extensions.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<Add />}>
          Install Plugin
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Extension sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">Plugin Management</Typography>
          </Box>
          <Typography color="textSecondary">
            Kubernetes plugin management functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default PluginsPage;