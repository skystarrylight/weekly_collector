// components/IssueTypeBadge.js
import React from 'react';
import { Chip } from '@mui/material';

function IssueTypeBadge({ type }) {
    const getColor = () => {
        switch (type) {
            case 'Epic':
                return 'purple';
            case 'Task':
                return 'blue';
            case 'Subtask':
                return 'green';
            case 'Story':
                return 'orange';
            default:
                return 'gray';
        }
    };

    return (
        <Chip
            label={type}
            style={{ backgroundColor: getColor(), color: 'white' }}
            size="small"
        />
    );
}

export default IssueTypeBadge;
