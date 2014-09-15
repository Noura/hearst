hearshties = {};

// find jQuery objects, assign event listeners
hearshties.init = function() {
    hearshties.api_headers = {
        'app_key':'bd4e742fb930b51e2e6637f415f1742f',
        'app_id':"26458f3f"
        } // todo: this probably shouldnt be in a plaintext js file lol
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
    $.ajax({
        url:'search',
        type:'post',
        data: {'q':user_query},
        success: function(response) {
            console.log(response)
        }
    })
};

window.onload = hearshties.init;

