import React from 'react';
import { Grid, TextField, FormControl, InputLabel, Select, MenuItem, Button } from '@mui/material';
import { Search } from '@mui/icons-material';

function SearchBar({ textInput, setTextInput, selectedOption, setSelectedOption, handleSearch }) {
    return (
        <>
            <Grid item xs={6}>
                <TextField
                    label="Search by Keyword"
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                    fullWidth
                    variant="outlined"
                />
            </Grid>
            <Grid item xs={3}>
                <FormControl fullWidth variant="outlined" size="small">
                    <InputLabel id="category-label">Category</InputLabel>
                    <Select
                        labelId="category-label"
                        value={selectedOption}
                        onChange={(e) => setSelectedOption(e.target.value)}
                        label="Category"
                    >
                        <MenuItem value="all">All</MenuItem>
                        <MenuItem value="epic">Epic</MenuItem>
                        <MenuItem value="task">Task</MenuItem>
                        <MenuItem value="subtask">Subtask</MenuItem>
                        <MenuItem value="story">Story</MenuItem>
                    </Select>
                </FormControl>
            </Grid>
            <Grid item xs={3}>
                <Button variant="contained" startIcon={<Search />} onClick={handleSearch} fullWidth>
                    Search
                </Button>
            </Grid>
        </>
    );
}

export default SearchBar;
