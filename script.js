async function getRecommendations() {
    const movie1 = document.getElementById('movie1').value;
    const movie2 = document.getElementById('movie2').value;
    const movie3 = document.getElementById('movie3').value;
    const movie4 = document.getElementById('movie4').value;

    const response = await fetch('http://127.0.0.1:8000/recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ movie1, movie2, movie3, movie4 }),
    });

    if (response.ok) {
        const data = await response.json();
        displayRecommendations(data.recommendations);
    } else {
        alert('Error fetching recommendations');
    }
}

function displayRecommendations(recommendations) {
    const recDiv = document.getElementById('recommendations');
    recDiv.innerHTML = '';  // Clear previous recommendations
    recommendations.forEach(movie => {
        const movieElement = document.createElement('p');
        movieElement.textContent = movie;
        recDiv.appendChild(movieElement);
    });
}
