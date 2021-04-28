import React from 'react';
import Axios from 'axios';
import { Chip, Typography, List, ListItem, Grid, CardMedia, Card, TextField, InputAdornment} from '@material-ui/core';
import './recipedetails.css';
class RecipeDetails extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            recipeDetails: {
                "_recipe_ingredients": [],
                "_recipe_instructions": [],
            },
            servings: 1,
            originalRecipeDetails:{},

        };
    }

    componentDidMount() {
        Axios.get(`/api/recipe_details?recipeid=${this.props.match.params.recipeID}`)
            .then(response => {
                this.setState({ 'recipeDetails': response.data });
                this.setState({'servings': response.data['_recipe_servings']});
                this.setState({'originalRecipeDetails': response.data});
                this.separateSentencesByPeriod();
            })
            .catch(err => {
                if (err.response.status === "404") {
                    console.log("404");
                }
            })
    }

    //Looks better if the first letters are capitalized so created a function for this
    capitalizeFirstLetter(input) {
        return input.charAt(0).toUpperCase() + input.slice(1);
    }

    separateSentencesByPeriod() {
        const newDetails = this.state.recipeDetails;
        if (newDetails["_recipe_instructions"][0]) { //check if there are actually instructions
            newDetails["_recipe_instructions"] = this.state.recipeDetails["_recipe_instructions"][0].split('.');
            this.setState({ 'recipeDetails': newDetails });
        }

    }

    getServings() {
        return this.state.servings;
    }

    //calculate how much to adjust ingredient amounts by to make new serving amounts
    calculateServingAdjustmentFactor() {
        const newServings = this.state.servings;
        const originalRecipe = this.state.originalRecipeDetails;
        const originalServings = originalRecipe['_recipe_servings'];
        const servingFactor = newServings/originalServings;
        return servingFactor;
    }

    render() {
        const RenderRecipeIngredients = this.state.recipeDetails["_recipe_ingredients"].map((ingredient, index) => {
            return (
                <>
                    <ListItem key={ingredient["_ingredient_id"]}>{this.calculateServingAdjustmentFactor()*ingredient["_ingredient_quantity"].toFixed(2) + ' ' + ingredient["_ingredient_unit"] + ' ' + this.capitalizeFirstLetter(ingredient["_ingredient_name"])}</ListItem>
                </>
            )
        });

        const RenderRecipeSteps = this.state.recipeDetails["_recipe_instructions"].map((step, index) => {
            return (
                <>
                    <ListItem key={index}>{step}</ListItem>
                </>
            )
        });

        const RenderRecipeTags = this.state.recipeDetails["_recipe_tags"] && this.state.recipeDetails["_recipe_tags"].map((tag) => {
            return (
                <>  <Grid item key={tag}>
                    <Chip label={tag} size="small" variant="default" />
                    </Grid>
                </>
            )
        });

        const HandlerChange = (event) => {
            if(!isNaN(event.target.value) && event.target.value > 0){
                this.setState({'servings': parseInt(event.target.value)});
            }
            this.calculateServingAdjustmentFactor();
        }

        return (
            <>
                <div className="recipe-page-content">
                    <Grid spacing='3' container>
                        <Grid item key='recipe-header-img'>
                            <Card>
                                <CardMedia component='img' image={this.state.recipeDetails["_recipe_image_url"]} alt="recipe image" />
                            </Card>
                        </Grid>

                        <Grid item key='recipe-info'>
                            <List>
                                <ListItem> <Typography variant="h4">{this.state.recipeDetails["_recipe_name"]}</Typography> </ListItem>
                                <ListItem> <Grid container>{RenderRecipeTags}</Grid> </ListItem>
                                <ListItem>
                                    <TextField
                                        label= "Servings"
                                        id="standard-multiline-flexible"
                                        defaultValue={this.getServings()}
                                        size='small'
                                        variant='outlined'
                                        onChange={HandlerChange}
                                        multiline
                                    />
                                </ListItem>
                                <ListItem> <Typography variant='body1'>{"Prep time: " + this.state.recipeDetails['_recipe_preparation_time'] + " minutes"}</Typography> </ListItem>

                            </List>

                        </Grid>

                        <Grid item key='recipe-ingredients'>
                            <Typography variant='h5'>Ingredients</Typography>
                            <div className="recipe-page-section-line" />
                            <List>
                                {RenderRecipeIngredients}
                            </List>

                        </Grid>

                        <Grid item key='recipe-steps'>
                            <div className="recipe-page-steps recipe-page-section">
                                <Typography variant='h5'>Steps</Typography>
                                <div className="recipe-page-section-line" />
                                <List>
                                    {RenderRecipeSteps}
                                </List>

                            </div>
                        </Grid>
                    </Grid>
                    </div>
            </>
        );
    }
}

export default RecipeDetails;