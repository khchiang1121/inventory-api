import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { Group, Add } from '@mui/icons-material';

const TenantsPage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Tenants
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage multi-tenant resource allocation and quotas.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<Add />}>
          Add Tenant
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Group sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">Tenant Management</Typography>
          </Box>
          <Typography color="textSecondary">
            Tenant management functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default TenantsPage;