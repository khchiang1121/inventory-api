import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { Computer, Add } from '@mui/icons-material';

const VirtualMachinesPage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Virtual Machines
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage virtual machine instances and lifecycle.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<Add />}>
          Create VM
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Computer sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">Virtual Machine Management</Typography>
          </Box>
          <Typography color="textSecondary">
            Virtual machine management functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default VirtualMachinesPage;