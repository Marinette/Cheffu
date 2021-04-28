import React from 'react';
import Axios from 'axios';
import Search from '../components/Search/Search';
import Results from '../components/Results/Results';
import './homepage.css';
import FilterTabs from '../components/Filters/FilterTabs';

class HomePage extends React.Component {

    constructor() {
        super();
        this.state = {
            ingredients: [],
            selectedIngredients: [],
            recipeResults:
                [],
            minCalorie: 0,
            maxCalorie: 9999,
            minCarbs: 0,
            maxCarbs: 9999,
            minProtein: 0,
            maxProtein: 9999,
            minFat: 0,
            maxFat: 9999,
            filtersEnabled: false,
        };
        this.SetFilterEnabled = this.SetFilterEnabled(this);
        this.SetFilterDisabled = this.SetFilterDisabled(this);
        this.GetSelected = this.GetSelected.bind(this);
        this.CheckAndSubmit = this.CheckAndSubmit.bind(this);

        this.SetMinCalorie = this.SetMinCalorie.bind(this);
        this.SetMaxCalorie = this.SetMaxCalorie.bind(this);
        this.FilterByCalorie = this.FilterByCalorie.bind(this);

        this.SetMinCarbs = this.SetMinCarbs.bind(this);
        this.SetMaxCarbs = this.SetMaxCarbs.bind(this);
        this.SetMinProtein = this.SetMinProtein.bind(this);
        this.SetMaxProtein = this.SetMaxProtein.bind(this);
        this.SetMinFat = this.SetMinFat.bind(this);
        this.SetMaxFat = this.SetMaxFat.bind(this);
        this.FilterByMacro = this.FilterByMacro.bind(this);
    }

    GetSelected = (selectIngredientNames) => {
        var temp = this.state.ingredients.filter(x => selectIngredientNames.includes(x["ingredientName"]));
        this.setState({ selectedIngredients: temp });
        return temp;
    }

    CheckAndSubmit = (key, value) => {
        const input = this.GetSelected(value);
        if (true) {
            // Do data processing for API JSON format if needed
            const variables = {
                ingredients: input
            }
            // API call and data processing
            Axios.post(`/api/search`, variables)
                .then(response => {
                    this.setState({ recipeResults: response.data });
                })
                .catch(err => {
                    if (err.response.status === "404") {
                        console.log("404");
                    }
                })
        }
    }

    SetMinCalorie = (event) => {
        this.setState({ minCalorie: event.currentTarget.value })
    }

    SetMaxCalorie = (event) => {
        this.setState({ maxCalorie: event.currentTarget.value })
    }

    FilterByCalorie = (key) => {
        if (key === "Enter") {
            var temp = "";
            for (let i = 0; i < this.state.recipeResults.length; i++) {
                if (i != this.state.recipeResults.length - 1) {
                    temp += this.state.recipeResults[i]["_recipe_id"] + ",";
                } else {
                    temp += this.state.recipeResults[i]["_recipe_id"];
                }
            }
            Axios.get(`/api/filter_by_calories?minCalories=${this.state.minCalorie}&maxCalories=${this.state.maxCalorie}&recipeIdList=${temp}`)
                .then(response => {
                    this.setState({ recipeResults: response.data });
                })
                .catch(err => {
                    if (err.response.status === "404") {
                        console.log("404");
                    }
                })
        }
    }

    SetMinCarbs = (event) => {
        this.setState({ minCarbs: event.currentTarget.value })
    }

    SetMaxCarbs = (event) => {
        this.setState({ maxCarbs: event.currentTarget.value })
    }

    SetMinProtein = (event) => {
        this.setState({ minProtein: event.currentTarget.value })
    }

    SetMaxProtein = (event) => {
        this.setState({ maxProtein: event.currentTarget.value })
    }

    SetMinFat = (event) => {
        this.setState({ minFat: event.currentTarget.value })
    }

    SetMaxFat = (event) => {
        this.setState({ maxFat: event.currentTarget.value })
    }

    FilterByMacro = (key) => {
        if (key === "Enter") {
            var temp = "";
            for (let i = 0; i < this.state.recipeResults.length; i++) {
                if (i != this.state.recipeResults.length - 1) {
                    temp += this.state.recipeResults[i]["_recipe_id"] + ",";
                } else {
                    temp += this.state.recipeResults[i]["_recipe_id"];
                }
            }
            Axios.get(`/api/filter_by_macros?minCarbs=${this.state.minCarbs}&maxCarbs=${this.state.maxCarbs}&minProtein=${this.state.minProtein}&maxProtein=${this.state.maxProtein}&minFat=${this.state.minFat}&maxFat=${this.state.maxFat}&recipeIdList=${temp}`)
                .then(response => {
                    this.setState({ recipeResults: response.data });
                })
                .catch(err => {
                    if (err.response.status === "404") {
                        console.log("404");
                    }
                })
        }
    }

    //enables filtering
    SetFilterEnabled = (event) => {
        this.setState({filterEnabled: true})
    }
    //disables filtering
    SetFilterDisabled = (event)=>{
        this.setState({filterEnabled: false})
    }
    componentDidMount() {
        // Need to find out the backend api route still
        Axios.get(`/api/get_ingredients`)
            .then(response => {
                this.setState({ ingredients: response.data });
            })
            .catch(err => {
                if (err.response.status === "404") {
                    console.log("404");
                }
            })
    }

    render() {
        return (<>
            <div className='homepage-content'>
                <div className='search'>
                    <Search
                        ingredients={this.state.ingredients}
                        GetSelected={this.GetSelected}
                        CheckAndSubmit={this.CheckAndSubmit}
                    />
                    <br></br>
                        <FilterTabs
                            FilterByCalorie={this.FilterByCalorie}
                            SetMinCalorie={this.SetMinCalorie}
                            SetMaxCalorie={this.SetMaxCalorie}
                            minCalorie={this.state.minCalorie}
                            maxCalorie={this.state.maxCalorie}

                            FilterByMacro={this.FilterByMacro}
                            SetMinCarbs={this.SetMinCarbs}
                            SetMaxCarbs={this.SetMaxCarbs}
                            minCarbs={this.state.minCarbs}
                            maxCarbs={this.state.maxCarbs}
                            SetMinProtein={this.SetMinProtein}
                            SetMaxProtein={this.SetMaxProtein}
                            minProtein={this.state.minProtein}
                            maxProtein={this.state.maxProtein}
                            SetMinFat={this.SetMinFat}
                            SetMaxFat={this.SetMaxFat}
                            minFat={this.state.minFat}
                            maxFat={this.state.maxFat}
                        />


                </div>
                <div className='results'>
                    <Results
                        recipeResults={this.state.recipeResults}
                    />
                </div>

            </div>
        </>);
    }
}

export default HomePage;