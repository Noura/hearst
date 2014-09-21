hearshties = {};

hearshties.keep_slide_id = 'first-slide';

hearshties.init = function() {

    hearshties.$intro_slide = $('#first-slide');
    hearshties.go_button = hearshties.go();

    // client-side templating
    // thanks Ned http://www.njl.us/
    hearshties.templates = {};
    $('script[type="underscore/template"]').each(function(){
        hearshties.templates[$(this).attr('id')] = _.template($(this).text());
    });

    hearshties.go_button.init();
};

// get culture, culture description from wikipedia, and images
hearshties.submit_user_query = function() {
    hearshties.go_button.loading();
    $.ajax({
        url:'/getculture',
        type:'GET',
        data: {},
        success: function(data) {
            console.log('data', data);
            // add a slide for each artifact
            var $slides = $('.slides');
            $slides.append(hearshties.templates.summary({
                'culture_name': data.culture_name,
                'culture_summary': data.culture_summary,
            }));
	    // add each artifact image as a slide 
            _.each(data.culture_data, function(img_url, id) {
                $slides.append(hearshties.templates.slide({
                    'img_url': img_url,
                }));
            });
            setTimeout(function() {
                hearshties.go_button.going(data.culture_name);
                setTimeout(function() {
                    // move explanatory page to the end of the slideshow and advance user to the culture description
                    Reveal.next();
                    hearshties.$intro_slide.remove();
                    $slides.append(hearshties.$intro_slide);
                    $(hearshties.$intro_slide.find('h1')[0]).html('Search again.')
                    hearshties.$intro_slide.find('p').remove();
                    hearshties.go_button.init();
                }, 1500);
            }, 100);
        },
        failure: function(data) {
            console.log('query failed with data', data);
            hearshties.go_button.init();
        }
    });
};

// manages the state of the go button
hearshties.go = function() {
    var that = {};
    that.$b = $('#go');
    that.$b.attr('class', '');
    that.ready = function() {
        return that.$b.attr('class') === '';
    };
    that.loading = function() {
        that.$b.attr('class', 'loading');
        that.$b.html('Loading...');
    };
    that.going = function(culture_name) {
        that.$b.attr('class', 'going');
        that.$b.html(culture_name + '!');
    };
    that.init= function() {
        that.$b = $('#go'); 
        that.$b.attr('class', '');
        hearshties.go_button.$b.on('click', function(ev) {
            if (!hearshties.go_button.ready()) {
                return;
            }
            hearshties.submit_user_query();
        });
        that.$b.html('Go');
    };
    return that;
};

window.onload = hearshties.init;

