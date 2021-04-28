import React, { Component } from "react";
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete'
import Chip from '@material-ui/core/Chip';
import {Typography, Container} from '@material-ui/core/';
import './search.css';

class Search extends Component {
    render() {
        return (
            <div className='search-bar'>
                <div className='search-bar-header'>
                    <Typography variant='h6'>Search for recipes</Typography>
                </div>
                <Autocomplete
                    freeSolo
                    multiple
                    autoSelect
                    id="tags-outlined"
                    options={this.props.ingredients.map((option) => option["ingredientName"])}
                    renderTags={(value, getTagProps) =>
                        value.map((option, index) => (
                            <Chip variant="outlined" label={option} {...getTagProps({ index })} />
                        ))
                    }
                    renderInput={(params) => <TextField {...params} label="Ingredients" variant="outlined" fullWidth />}

                    onChange={(event, value) => this.props.CheckAndSubmit(event.key,value)}

                />
            </div>
        )
    }
}


export default Search;