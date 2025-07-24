import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { ViewModule, Add } from '@mui/icons-material';

const RacksPage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Racks
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage server racks and their configurations.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<Add />}>
          Add Rack
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <ViewModule sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">Rack Management</Typography>
          </Box>
          <Typography color="textSecondary">
            Rack management functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default RacksPage;