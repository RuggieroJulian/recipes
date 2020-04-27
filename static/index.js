document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#form').onsubmit = () => {

        const parentElement = document.getElementById('result');

        // Initialize new request
        const request = new XMLHttpRequest();
        //const meal_type = document.querySelector('#meal_type').value;
        const meal_type = document.getElementById('meal_type').value;
        const ingredient = document.getElementById('ingredients').value;
        console.log(meal_type);
        console.log(ingredient);
        request.open('POST', '/convert');

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);
            // Update the result div
            if (data.success) {
                parentElement.innerHTML="";
                
                // Add child elements
                for (let recipe of data.data) {
                    //has the ingredient
                    const childElement = document.createElement('div');
                    appendChildElement = parentElement.appendChild(childElement);
                    appendChildElement.innerHTML = recipe.RecipeTitle;
                }

                //const contents = 3;// `${data.RecipeTitle}`;
               //document.querySelector('#result').innerHTML = contents;
            }
            else {
                document.querySelector('#result').innerHTML = 'There was an error.';
            }
        }

        // Add data to send with request
        const data = new FormData();
        data.append('ingredient', ingredient);
        data.append('meal_type', meal_type);

        // Send request
        request.send(data);
        return false;
    };

});
