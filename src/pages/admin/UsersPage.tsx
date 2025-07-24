import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { People, Add } from '@mui/icons-material';

const UsersPage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Users
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage user accounts and access controls.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<Add />}>
          Add User
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <People sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">User Management</Typography>
          </Box>
          <Typography color="textSecondary">
            User management functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default UsersPage;