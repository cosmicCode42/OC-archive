document.addEventListener('DOMContentLoaded', function() {
    // sidenav initialisation
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);
    
    // select initialisation
    let selects = document.querySelectorAll('select');
    M.FormSelect.init(selects);

    // collapsible initialisation
    let collapsibles = document.querySelectorAll('.collapsible');
    M.Collapsible.init(collapsibles);

    // display/hide Add New Genre option in character creation page
    const genreSelect = document.getElementById('genre_id');
    const newGenreInput = document.getElementById('new_genre_input');

    genreSelect.addEventListener('change', function() {
        if (genreSelect.value === 'new_genre') {
            newGenreInput.style.display = 'block';
        } else {
            newGenreInput.style.display = 'none';
        }
    });
  });