import React from 'react';
import PropTypes from 'prop-types';
import SwipeableViews from 'react-swipeable-views';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import CalorieFilter from './CalorieFilter';
import MacroFilter from './MacroFilter';
import FilterListIcon from '@material-ui/icons/FilterList';
import {ToggleButton,Container,Box,Typography} from '@material-ui/core'

function TabPanel(props) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`full-width-tabpanel-${index}`}
            aria-labelledby={`full-width-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Container>
                    <Box p={3}>
                        {/* <Typography>{children}</Typography> */}
                        {children}
                    </Box>
                </Container>
            )}
        </div>
    );
}

TabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.any.isRequired,
    value: PropTypes.any.isRequired,
};

function a11yProps(index) {
    return {
        id: `full-width-tab-${index}`,
        'aria-controls': `full-width-tabpanel-${index}`,
    };
}

const useStyles = makeStyles((theme) => ({
    root: {
        backgroundColor: theme.palette.background.paper,
        width: 500,
    },
}));

export default function FilterTabs(props) {
    const classes = useStyles();
    const theme = useTheme();
    const [value, setValue] = React.useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    const handleChangeIndex = (index) => {
        setValue(index);
    };

    return (
        <div className={classes.root} style={{width: "100%"}}>
            <AppBar position="static" color="default">
                <Tabs
                    value={value}
                    onChange={handleChange}
                    indicatorColor="primary"
                    textColor="primary"
                    variant="fullWidth"
                    aria-label="full width tabs"
                >   <Tab icon={<FilterListIcon/>}/>
                    <Tab label="Calories" {...a11yProps(0)} />
                    <Tab label="Macros" {...a11yProps(1)} />
                </Tabs>
            </AppBar>
            <SwipeableViews
                axis={theme.direction === 'rtl' ? 'x-reverse' : 'x'}
                index={value}
                onChangeIndex={handleChangeIndex}
            >
            <TabPanel value={value} index={0} dir={theme.direction}>

            </TabPanel>
                <TabPanel value={value} index={1} dir={theme.direction}>
                    <CalorieFilter
                        SetMinCalorie={props.SetMinCalorie}
                        SetMaxCalorie={props.SetMaxCalorie}
                        FilterByCalorie={props.FilterByCalorie}
                        minCalorie={props.minCalorie}
                        maxCalorie={props.maxCalorie}
                    />
                </TabPanel>
                <TabPanel value={value} index={2} dir={theme.direction}>
                    <MacroFilter
                        FilterByMacro={props.FilterByMacro}
                        SetMinCarbs={props.SetMinCarbs}
                        SetMaxCarbs={props.SetMaxCarbs}
                        minCarbs={props.minCarbs}
                        maxCarbs={props.maxCarbs}
                        SetMinProtein={props.SetMinProtein}
                        SetMaxProtein={props.SetMaxProtein}
                        minProtein={props.minProtein}
                        maxProtein={props.maxProtein}
                        SetMinFat={props.SetMinFat}
                        SetMaxFat={props.SetMaxFat}
                        minFat={props.minFat}
                        maxFat={props.maxFat}
                    />
                </TabPanel>
            </SwipeableViews>
        </div>
    );
}