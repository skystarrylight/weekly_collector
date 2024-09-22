// components/AssigneeBadge.js
import React from 'react';
import { Avatar, Chip } from '@mui/material';

function AssigneeBadge({ assignee }) {
    if (assignee === 'Unassigned') return <Chip label="Unassigned" size="small" />;

    const initials = assignee.split(' ').map((name) => name[0]).join('');

    return (
        <Chip
            avatar={<Avatar>{initials}</Avatar>}
            label={assignee}
            size="small"
        />
    );
}

export default AssigneeBadge;
