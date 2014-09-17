hearshties = {};

hearshties.init = function() {

    // client-side templating
    // thanks Ned http://www.njl.us/
    hearshties.templates = {};
    $('script[type="underscore/template"]').each(function(){
        hearshties.templates[$(this).attr('id')] = _.template($(this).text());
    });

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
            $('#search-button').hide()
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
            $('#search-button').show()
            console.log('response', response);
            var data = JSON.parse(response);
            console.log('data', data);
            $('.slides section').each(function() {
                var $this = $(this);
                if ($this.attr('id') !== 'search-outer') {
                    $this.remove();
                }
            });
            var $slides = $('.slides');
            _.each(data.artifacts, function(d) {
                $slides.append(hearshties.templates.slide(d));
            });
            if (data.artifacts.length > 0) {
                setTimeout(function() { Reveal.next() }, 200)
            }
        }
    })
};

window.onload = hearshties.init;

