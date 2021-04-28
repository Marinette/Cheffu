import React from "react";
import TextField from '@material-ui/core/TextField';
import './filter.css';
import Grid from "@material-ui/core/Grid";

class MacroFilter extends React.Component {

    render() {
        return (
            <>
                <div className="filter-main">
                    <form onKeyDown={(event) => this.props.FilterByMacro(event.key)}>
                    <Grid container spacing={2} className="filter-fields" direction='row' justify='center' alignItems='center'>
                        
                            <Grid item key="carb-min"><div className="filter-form-item">
                                <TextField
                                    id="minCarbs"
                                    type="number"
                                    label="Minimum Carbs"
                                    value={this.props.minCarbs}
                                    onChange={(event) => this.props.SetMinCarbs(event)}
                                />
                            </div></Grid>
                            <Grid item key="carb-max">
                                <div className="filter-form-item">
                                    <TextField
                                        id="maxCarbs"
                                        type="number"
                                        label="Maximum Carbs"
                                        value={this.props.maxCarbs}
                                        onChange={(event) => this.props.SetMaxCarbs(event)}
                                    />
                                </div>
                            </Grid>
                            <Grid item key="protein-min">                                <div className="filter-form-item">
                                <TextField
                                    id="minProtein"
                                    type="number"
                                    label="Minimum Protein"
                                    value={this.props.minProtein}
                                    onChange={(event) => this.props.SetMinProtein(event)}
                                />
                            </div></Grid>
                            <Grid item key="protein-max">                                <div className="filter-form-item">
                                <TextField
                                    id="maxProtein"
                                    type="number"
                                    label="Maximum Protein"
                                    value={this.props.maxProtein}
                                    onChange={(event) => this.props.SetMaxProtein(event)}
                                />
                            </div></Grid>
                            <Grid item key="fat-min">                                <div className="filter-form-item">
                                <TextField
                                    id="minFat"
                                    type="number"
                                    label="Minimum Fat"
                                    value={this.props.minFat}
                                    onChange={(event) => this.props.SetMinFat(event)}
                                />
                            </div></Grid>
                            <Grid item key="fat-max">                                <div className="filter-form-item">
                                <TextField
                                    id="maxFat"
                                    type="number"
                                    label="Maximum Fat"
                                    value={this.props.maxFat}
                                    onChange={(event) => this.props.SetMaxFat(event)}
                                />
                            </div></Grid>
                       
                    </Grid>
                    </form>

                </div>
            </>
        );
    }
}

export default MacroFilter;
