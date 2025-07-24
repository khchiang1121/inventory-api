import React from 'react';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { Settings, Save } from '@mui/icons-material';

const SettingsPage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Settings
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Configure application settings and preferences.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<Save />}>
          Save Settings
        </Button>
      </Box>

      <Card>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            <Settings sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">Application Settings</Typography>
          </Box>
          <Typography color="textSecondary">
            Settings management functionality will be implemented here.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default SettingsPage;