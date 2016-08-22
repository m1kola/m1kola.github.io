jQuery(document).ready(function($) {
    var MQL = 1170;

    // Primary navigation slide-in effect
    if ($(window).width() > MQL) {
        var headerHeight = $('#common_navbar').height();
        $(window).on(
            'scroll',
            {
                previousTop: 0
            },
            function() {
                var currentTop = $(window).scrollTop();
                var $navbar = $('.navbar-custom');

                // Check if user is scrolling up
                if (currentTop < this.previousTop) {
                    // If scrolling up...
                    if (currentTop > 0 && $navbar.hasClass('is-fixed')) {
                        $navbar.addClass('is-visible');
                    } else {
                        $navbar.removeClass('is-visible is-fixed');
                    }
                } else {
                    // If scrolling down...
                    $navbar.removeClass('is-visible');
                    if (currentTop > headerHeight && !$navbar.hasClass('is-fixed')) $navbar.addClass('is-fixed');
                }

                this.previousTop = currentTop;
            }

        );
    }
});
