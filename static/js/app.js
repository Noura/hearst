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
        }
    });

    hearshties.$search_button.on('click', function(ev) {
        hearshties.submit_user_query(hearshties.$search.val());
    });
};

hearshties.submit_user_query = function(user_query) {
    $.ajax({
        url:'getculture',
        type:'get',
        data: {'q':user_query},
        success: function(data) {
            console.log('data', data);
            $('.slides section').each(function() {
                var $this = $(this);
                if ($this.attr('id') !== 'search-outer') {
                    $this.remove();
                }
            });
            var $slides = $('.slides');
            console.log('data.artifacts', data.artifacts);
            _.each(data.artifacts, function(img_url, id) {
                $slides.append(hearshties.templates.slide({
                    'img_url': img_url,
                }));
            });
            if (data.artifacts.length > 0) {
                setTimeout(function() {
                    Reveal.next();
                }, 500);
            }
        }
    })
};

window.onload = hearshties.init;

