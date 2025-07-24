import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { Security, Add } from '@mui/icons-material';

const PermissionsPage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Permissions
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage user permissions and access controls.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<Add />}>
          Add Permission
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Security sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">Permission Management</Typography>
          </Box>
          <Typography color="textSecondary">
            Permission management functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default PermissionsPage;