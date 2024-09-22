import React from 'react';
import { Box, Chip } from '@mui/material';

const assigneeOptions = ['louie.han', 'dahlia.n', 'dylan.1', 'bay.cloudy', 'jenn.y', 'akira.toya', 'zet.woo', 'imo.boo'];

function AssigneeChips({ selectedAssignees, setSelectedAssignees }) {
    const handleAssigneeClick = (assignee) => {
        if (selectedAssignees.includes(assignee)) {
            setSelectedAssignees(selectedAssignees.filter((a) => a !== assignee));
        } else {
            setSelectedAssignees([...selectedAssignees, assignee]);
        }
    };

    return (
        <Box display="flex" flexWrap="wrap" gap={1} style={{ marginBottom: '10px' }}>
            {assigneeOptions.map((assignee) => (
                <Chip
                    key={assignee}
                    label={assignee}
                    color={selectedAssignees.includes(assignee) ? 'primary' : 'default'}
                    onClick={() => handleAssigneeClick(assignee)}
                    style={{ cursor: 'pointer' }}
                />
            ))}
        </Box>
    );
}

export default AssigneeChips;
