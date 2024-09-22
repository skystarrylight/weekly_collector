import React from 'react';
import { Avatar, Tooltip } from '@mui/material';

const UserAvatar = ({ name }) => {
    const initials = name.split(' ').map((n) => n[0]).join('').toUpperCase();

    return (
        <Tooltip title={name}>
            <Avatar>{initials}</Avatar>
        </Tooltip>
    );
};

export default UserAvatar;
