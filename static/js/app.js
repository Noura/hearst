hearshties = {};

hearshties.keep_slide_id = 'first-slide';

hearshties.init = function() {

    hearshties.go_button = hearshties.go();

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

    hearshties.go_button.$b.on('click', function(ev) {
        if (!hearshties.go_button.ready()) {
            return;
        }
        hearshties.submit_user_query();
    });
};

hearshties.submit_user_query = function() {
    hearshties.go_button.loading();
    $.ajax({
        url:'/getculture',
        type:'GET',
        data: {},
        success: function(data) {
            console.log('data', data);
            // remove everything except the first (title) slide
            $('.slides section').each(function() {
                var $this = $(this);
                if ($this.attr('id') !== 'first-slide') {
                    $this.remove();
                }
            });
            // add a slide for each artifact 
            var $slides = $('.slides');
            _.each(data.artifacts, function(img_url, id) {
                $slides.append(hearshties.templates.slide({
                    'img_url': img_url,
                }));
                console.log(img_url)
            });
            setTimeout(function() {
                hearshties.go_button.going(data.culture_name);
                setTimeout(function() {
                    Reveal.next();
                    hearshties.go_button.reset();
                }, 1500);
            }, 3000);
        },
        failure: function(data) {
            console.log('query failed with data', data);
            hearshties.go_button.reset();
        }
    });
};

hearshties.go = function() {
    var that = {};
    that.$b = $('#go');
    that.ready = function() {
        return that.$b.data('state') === '';
    };
    that.loading = function() {
        that.$b.data('state', 'loading');
        that.$b.html('Loading...');
    };
    that.going = function(culture_name) {
        that.$b.data('state', 'going');
        that.$b.html(culture_name + '!');
    };
    that.reset = function() {
        that.$b.data('state', '');
        that.$b.html('Go');
    };
    return that;
};

window.onload = hearshties.init;

