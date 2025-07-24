import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Grid,
} from '@mui/material';
import { Storage, Add } from '@mui/icons-material';

const DataCentersPage: React.FC = () => {
  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Data Centers
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage your data center infrastructure and facilities.
          </Typography>
        </Box>
        <Button variant="contained" startIcon={<Add />}>
          Add Data Center
        </Button>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Storage sx={{ mr: 2, color: 'primary.main' }} />
                <Typography variant="h6">Data Centers Management</Typography>
              </Box>
              <Typography color="textSecondary">
                This page will contain data center management functionality including:
              </Typography>
              <Box component="ul" sx={{ mt: 2 }}>
                <li>View all data centers</li>
                <li>Add/Edit/Delete data centers</li>
                <li>Monitor data center capacity and utilization</li>
                <li>Manage rooms and rack allocations</li>
                <li>Track power and cooling systems</li>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DataCentersPage;