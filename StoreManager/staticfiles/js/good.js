        $(document).ready(function() {
            $('#add-good-button').click(function() {
                $('#add-good-modal').show();
            });

            $('.close').click(function() {
                $('#add-good-modal').hide();
            });

            $(window).click(function(event) {
                if (event.target.id === 'add-good-modal') {
                    $('#add-good-modal').hide();
                }
            });
        });