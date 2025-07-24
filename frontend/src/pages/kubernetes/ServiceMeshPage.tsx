import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { Hub, Add } from '@mui/icons-material';

const ServiceMeshPage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Service Mesh
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage service mesh configurations and deployments.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<Add />}>
          Deploy Service Mesh
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Hub sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">Service Mesh Management</Typography>
          </Box>
          <Typography color="textSecondary">
            Service mesh management functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ServiceMeshPage;