import React from "react";
import TextField from '@material-ui/core/TextField';
import './filter.css';


class CalorieFilter extends React.Component {

    render() {
        return (
            <>
                <div className="filter-main">
                    <div className="filter-fields">
                        <form onKeyDown={(event) => this.props.FilterByCalorie(event.key)}>
                            <div className="filter-form">
                                <div className="filter-form-item">
                                    <TextField 
                                        id="minCalorie" 
                                        type="number"
                                        label="Minimum Calorie" 
                                        value={this.props.minCalorie}
                                        onChange={(event) => this.props.SetMinCalorie(event)}
                                    />
                                </div>
                                <div className="filter-form-item">
                                    <TextField 
                                        id="maxCalorie" 
                                        type="number"
                                        label="Maximum Calorie" 
                                        value={this.props.maxCalorie}
                                        onChange={(event) => this.props.SetMaxCalorie(event)}
                                    />
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </>
        );
    }
}

export default CalorieFilter;
