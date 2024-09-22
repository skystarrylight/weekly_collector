import React, { useState } from 'react';
import { TableRow, TableCell, IconButton } from '@mui/material';
import { ExpandLess, ExpandMore } from '@mui/icons-material';
import StatusBadge from './StatusBadge';
import UserAvatar from './UserAvatar';

const IssueRow = ({ issue, issueKey, level }) => {
    const [isOpen, setIsOpen] = useState(true);

    const toggleOpen = () => setIsOpen(!isOpen);

    return (
        <>
            <TableRow style={{ paddingLeft: `${level * 20}px` }}>
                <TableCell>
                    {issue.tasks && (
                        <IconButton onClick={toggleOpen}>
                            {isOpen ? <ExpandLess /> : <ExpandMore />}
                        </IconButton>
                    )}
                </TableCell>
                <TableCell>{issueKey}</TableCell>
                <TableCell>{issue.summary}</TableCell>
                <TableCell><StatusBadge status={issue.status} /></TableCell>
                <TableCell><UserAvatar name={issue.assignee} /></TableCell>
                <TableCell>{issue.due_date || 'N/A'}</TableCell>
                <TableCell>{issue.labels.join(', ') || 'None'}</TableCell>
                <TableCell>{issue.created || 'N/A'}</TableCell>
                <TableCell>{issue.updated || 'N/A'}</TableCell>
                <TableCell>{issue.reporter}</TableCell>
            </TableRow>
            {isOpen && issue.tasks &&
                Object.keys(issue.tasks).map((taskKey) => (
                    <IssueRow key={taskKey} issue={issue.tasks[taskKey]} issueKey={taskKey} level={level + 1} />
                ))}
            {isOpen && issue.subtasks &&
                Object.keys(issue.subtasks).map((subtaskKey) => (
                    <IssueRow key={subtaskKey} issue={issue.subtasks[subtaskKey]} issueKey={subtaskKey} level={level + 1} />
                ))}
        </>
    );
};

export default IssueRow;
