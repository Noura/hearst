hearshties = {};

// find jQuery objects, assign event listeners
hearshties.init = function() {
    hearshties.$search = $('#search');
    hearshties.$search_button = $('#search-button');

    hearshties.$search.on('keyup', function(ev) {
        if(ev.keyCode === 13) {
            console.log('submitting', hearshties.$search.val());
            hearshties.submit_user_query(hearshties.$search.val());
        }
    });

    hearshties.$search_button.on('click', function(ev) {
        hearshties.submit_user_query(hearshties.$search.val());
    });
};

hearshties.submit_user_query = function(user_query) {
    alert('got user query ' + user_query);
};

window.onload = hearshties.init;

