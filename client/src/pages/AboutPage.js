import React from 'react';
import { Grid, Avatar, Typography, Card, CardContent, Chip } from '@material-ui/core';
import marinette from '../images/marinette-icon.jpg';
class AboutPage extends React.Component {

    constructor() {
        super();
        this.state = {
            info: [
                {
                    'name': 'Sheng Zhao',
                    'role': 'Frontend Dev',
                    'image': '../images/zac-icon.png'
                },
                {
                    'name': 'Marinette Chen',
                    'role': 'Frontend Dev',
                    'image': {marinette}
                },
                {
                    'name': 'Abhishek Arya',
                    'role': 'Backend Dev',
                    'image': '../images/abhi-icon.png'
                },
                {
                    'name': 'David Zhang',
                    'role': 'Backend Dev',
                    'image': '../images/david-icon.png'
                }
            ]


        }
    }

    renderProfiles() {
        return this.state.info.map(
            (profile) => {
                return (
                    <>
                        <Grid item key={profile['name']}>
                            <Card>
                                <CardContent>
                                    <Avatar size='large' src={profile['name']} />
                                    <Typography variant='h6'>{profile['name']}</Typography>
                                    <Chip variant='default' label={profile['role']} />
                                </CardContent>

                            </Card>
                        </Grid>

                    </>
                )
            }
        )
    }
    render() {
        return (<>
            <div>
                <Grid container spacing={3}>
                    {this.renderProfiles()}
                </Grid>
            </div>
        </>);
    }
}

export default AboutPage;