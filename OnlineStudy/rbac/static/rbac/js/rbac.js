(function (jq) {
    jq('.multi-menu .title').click(function () {
        $(this).next().toggleClass('hide');
    });
})(jQuery);