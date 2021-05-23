const search = document.getElementById('search');
const matchList = document.getElementById('match-list');

// searches in df and filters 
const searchPlayer = async searchText => {
    const res = await fetch('/static/javascript/json_dfteam.json');
    const teams = await res.json();

    // Get matches to current input 
    let matches = teams.filter(team => {
        const regex = new RegExp(`^${searchText}`,'gi');
        return team.str_team_name.match(regex)
    });
    if (searchText.length === 0) {
        matches = [];
        matchList.innerHTML = '';
    }

    outputHtml(matches)
};

const outputHtml = matches => {
    if(matches.length > 0 )
    {
        const html = matches.map(match => `
        <a class="card card-body mb-1" href="/teams/${match.int_team_id-1}">
        <h4>${match.str_team_name}<span class="text-primary">
        ${match.int_team_id}</span></h4>
        </a>
        ` )
        .join('');


        matchList.innerHTML = html;
    }
}


search.addEventListener('input', function(event) { 
    searchPlayer(search.value);
} );
