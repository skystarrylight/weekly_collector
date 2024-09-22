import React from 'react';
import { Chip } from '@mui/material';

const StatusBadge = ({ status }) => {
    const color = status === 'In Progress' ? 'primary' : 'default';
    return <Chip label={status} color={color} />;
};

export default StatusBadge;
