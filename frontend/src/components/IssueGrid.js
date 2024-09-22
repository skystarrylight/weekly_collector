import React, { useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { Paper, Typography } from '@mui/material';
import { IssueTypeBadge, StatusBadge, AssigneeBadge } from './Badges';

function IssueGrid({ data }) {
    // 데이터를 트리 구조로 변환
    const transformDataToTree = (data) => {
        const rows = [];
        Object.keys(data).forEach((issueKey) => {
            const epic = data[issueKey];

            rows.push({
                id: issueKey,
                key: issueKey,
                summary: epic.summary,
                status: epic.status,
                assignee: epic.assignee,
                type: epic.type,
                due_date: epic.due_date || 'N/A',
                parent: null  // 에픽은 부모가 없음
            });

            if (epic.tasks) {
                Object.keys(epic.tasks).forEach((taskKey) => {
                    const task = epic.tasks[taskKey];

                    rows.push({
                        id: taskKey,
                        key: taskKey,
                        summary: task.summary,
                        status: task.status,
                        assignee: task.assignee,
                        type: task.type,
                        due_date: task.due_date || 'N/A',
                        parent: issueKey  // 태스크는 에픽이 부모
                    });

                    if (task.subtasks) {
                        Object.keys(task.subtasks).forEach((subtaskKey) => {
                            const subtask = task.subtasks[subtaskKey];

                            rows.push({
                                id: subtaskKey,
                                key: subtaskKey,
                                summary: subtask.summary,
                                status: subtask.status,
                                assignee: subtask.assignee,
                                type: subtask.type,
                                due_date: subtask.due_date || 'N/A',
                                parent: taskKey  // 서브태스크는 태스크가 부모
                            });
                        });
                    }
                });
            }
        });
        return rows;
    };

    const rows = useMemo(() => transformDataToTree(data), [data]);

    // 컬럼 정의
    const columns = useMemo(() => [
        { headerName: 'Key', field: 'key', width: 150 },
        { headerName: 'Parent', field: 'parent', width: 150 },
        { headerName: 'Summary', field: 'summary', width: 650 },
        {
            headerName: 'Issue Type',
            field: 'type',
            width: 150,
            cellRenderer: (params) => <IssueTypeBadge type={params.value} />
        },
        {
            headerName: 'Status',
            field: 'status',
            width: 150,
            cellRenderer: (params) => <StatusBadge status={params.value} />
        },
        {
            headerName: 'Assignee',
            field: 'assignee',
            width: 200,
            cellRenderer: (params) => <AssigneeBadge assignee={params.value} />
        },
        { headerName: 'Due Date', field: 'due_date', width: 150 }
    ], []);

    // 트리 데이터와 관련된 설정
    const autoGroupColumnDef = {
        headerName: 'Group',
        field: 'parent',
        cellRenderer: 'agGroupCellRenderer',
        cellRendererParams: {
            suppressCount: true // 그룹 항목 개수 숨김
        }
    };

    return (
        <Paper className="data-table" elevation={3} style={{ marginTop: '40px', height: 600 }}>
            {rows.length === 0 ? (
                <Typography variant="h6" color="textSecondary" align="center" style={{ padding: '20px' }}>
                    No data to display.
                </Typography>
            ) : (
                <div className="ag-theme-alpine" style={{ height: 600, width: '100%' }}>
                    <AgGridReact
                        rowData={rows}
                        columnDefs={columns}
                        autoGroupColumnDef={autoGroupColumnDef}
                        treeData={true} // 트리 구조 사용
                        getDataPath={(data) => {
                            console.log("Tree data:", data); // 데이터를 콘솔에 출력
                            return data.parent ? [data.parent, data.id] : [data.id];
                        }}
                        groupDefaultExpanded={-1} // 모든 그룹 기본 확장
                        animateRows={true}
                    />
                </div>
            )}
        </Paper>
    );
}

export default IssueGrid;