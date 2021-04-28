import React from "react";
import { Card, colors, Container } from "@material-ui/core";
import CardMedia from "@material-ui/core/CardMedia";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import './results.css';


class Results extends React.Component {
    GenerateCards() {
        if (this.props.recipeResults) {
            return this.props.recipeResults.map((result) => (
                <Grid item key={result["_recipe_id"]}>
                    <Card variant="outlined" style={{ width: "90%", height: "90%" }}>
                        {/* <a href={result["recipeURL"]}> */}
                        <a href={`/recipe/${result["_recipe_id"]}`}>
                            <CardActionArea>
                                <CardContent>
                                    <Typography>{result["_recipe_name"]}</Typography>
                                </CardContent>
                                <CardMedia
                                    style={{ height: 250, width: 250 }}
                                    image={result["_recipe_image_url"]}
                                    title={result["_recipe_name"]}
                                />
                            </CardActionArea>
                        </a>
                    </Card>
                </Grid>
            ));
        }
    }

    render() {
        return (
            <>
                <Container className="recipe-results">
                    <Typography variant='h4' style={{textAlign: "center"}}> Results </Typography>
                    <Container className="results-panel">
                        {
                            this.props.recipeResults.length > 0 ? 
                            <div className="card-area">
                                <Grid container spacing={3} className="search-results-grid">
                                    {this.GenerateCards()}
                                </Grid>
                            </div>
                            :
                            <Typography variant='body2' style={{textAlign: "center"}}>You have not searched for anything or nothing met the search criteria.</Typography>
                        }
                    </Container>
                </Container>
            </>
        );
    }
}

export default Results;
