import React, { useState } from 'react';
import { Paper, Typography, Grid } from '@mui/material';
import SearchBar from './components/SearchBar';
import AssigneeChips from './components/AssigneeChips';
import IssueGrid from './components/IssueGrid';
import './App.css';  // 스타일 파일

function App() {
    const [textInput, setTextInput] = useState('');
    const [selectedOption, setSelectedOption] = useState('all');
    const [selectedAssignees, setSelectedAssignees] = useState([]);
    const [data, setData] = useState([]);

    // API 호출
    const handleSearch = async () => {
        try {
            const projectKey = 'AIP';
            let url = `http://localhost:8000/project/${projectKey.toString()}`;
            const queryParams = new URLSearchParams({
                keyword: textInput,
                assignees: selectedAssignees.join(',')
            });

            switch (selectedOption) {
                case 'all':
                    url += `/hierarchy?${queryParams.toString()}`;
                    break;
                case 'epic':
                    url += `/epics?${queryParams.toString()}`;
                    break;
                case 'task':
                    url += `/tasks?${queryParams.toString()}`;
                    break;
                case 'subtask':
                    url += `/subtasks?${queryParams.toString()}`;
                    break;
                case 'story':
                    url += `/stories?${queryParams.toString()}`;
                    break;
                default:
                    break;
            }

            const response = await fetch(url);
            const result = await response.json();
            setData(result);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    return (
        <div className="app-container">
            <Paper className="form-container" elevation={3}>
                <Typography variant="h4" gutterBottom>Boulanger Issue Tracker</Typography>
                <Grid container spacing={2} alignItems="center" style={{ marginBottom: '10px' }}>
                    <SearchBar
                        textInput={textInput}
                        setTextInput={setTextInput}
                        selectedOption={selectedOption}
                        setSelectedOption={setSelectedOption}
                        handleSearch={handleSearch}
                    />
                </Grid>
                <Grid container spacing={2} style={{ marginTop: '10px' }}>
                    <AssigneeChips
                        selectedAssignees={selectedAssignees}
                        setSelectedAssignees={setSelectedAssignees}
                    />
                </Grid>
            </Paper>
            <IssueGrid data={data} />
        </div>
    );
}

export default App;
