import React from 'react';
import { Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material';
import IssueRow from './IssueRow';

const IssueTable = ({ data }) => {
    return (
        <Table>
            <TableHead>
                <TableRow>
                    <TableCell>Type</TableCell>
                    <TableCell>Key</TableCell>
                    <TableCell>Summary</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Assignee</TableCell>
                    <TableCell>Due Date</TableCell>
                    <TableCell>Labels</TableCell>
                    <TableCell>Created</TableCell>
                    <TableCell>Updated</TableCell>
                    <TableCell>Reporter</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {Object.keys(data).map((epicKey) => (
                    <IssueRow key={epicKey} issue={data[epicKey]} issueKey={epicKey} level={0} />
                ))}
            </TableBody>
        </Table>
    );
};

export default IssueTable;
