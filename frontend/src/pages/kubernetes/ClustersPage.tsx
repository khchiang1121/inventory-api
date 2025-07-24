import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { Cloud, Add } from '@mui/icons-material';

const ClustersPage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Kubernetes Clusters
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage Kubernetes cluster lifecycle and configurations.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<Add />}>
          Create Cluster
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Cloud sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">Cluster Management</Typography>
          </Box>
          <Typography color="textSecondary">
            Kubernetes cluster management functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ClustersPage;