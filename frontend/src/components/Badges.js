import React from 'react';
import { Chip } from '@mui/material';

// 이슈 타입 배지
export const IssueTypeBadge = ({ type }) => {
    return (
        <Chip
            label={type}
            className={`issue-badge ${type.toLowerCase()}`}
            size="small"
            style={{ backgroundColor: type === 'Epic' ? 'purple' : type === 'Task' ? 'blue' : 'green', color: 'white' }}
        />
    );
};

// 상태 배지
export const StatusBadge = ({ status }) => {
    const color = status === 'In Progress' ? 'orange' : 'green';
    return (
        <Chip
            label={status}
            className="status-badge"
            size="small"
            style={{ backgroundColor: color, color: 'white' }}
        />
    );
};

// 어싸인 배지
export const AssigneeBadge = ({ assignee }) => {
    return (
        <Chip
            label={assignee === 'Unassigned' ? 'Unassigned' : assignee}
            className="assignee-badge"
            size="small"
            style={{ backgroundColor: assignee === 'Unassigned' ? 'gray' : 'blue', color: 'white' }}
        />
    );
};
