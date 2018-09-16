$(document).ready(function () {

    /* ======================= Contact Form =============*/
    var contactForm = $('.contact_form_ajax');

    var contactActionEndPoint = contactForm.attr('action'),
        contactMethod = contactForm.attr('method')
        // contactBtn = cantactForm.find("[type='submit']")

    function displaySubmiting(submitBtn, defaultText, submiting){
        if (submiting){
            submitBtn.addClass('disable')
            submitBtn.html("<i class='fa fa-span fa-spinner'></i> Sending...")
        } else {
            submitBtn.removeClass('disable')
            submitBtn.html(defaultText)
        }
    }

    contactForm.submit(function (e) {
        e.preventDefault()
        var thisForm = $(this);
        var contactFormData = thisForm.serialize(),
            contactBtn = thisForm.find("[type='submit']"),
            contactFormtext = contactBtn.text()

        displaySubmiting(contactBtn, '', true)

        $.ajax({
            url: contactActionEndPoint,
            method: contactMethod,
            data: contactFormData,
            success: function(data) {
                var thisform = $(this)
                contactForm[0].reset()
                // alert('Thanks for submiting')
                console.log(data)
                setTimeout(function () {
                    displaySubmiting(contactBtn, contactFormtext, false)
                }, 2000)
            },
            error: function(errorData) {
                console.log('contact Error')
                alert('An error occured')
                console.log(errorData.error)
                setTimeout(function () {
                    displaySubmiting(contactBtn, contactFormtext, false)
                }, 2000)
            },
        });
    });



    /* ======================= search =============*/
    var searchForm = $('.search-form-ajax'),
        searchInput = searchForm.find("[name='q']"), // input name name=q
        typingTimer,
        typingInterval = 1500, // .5 seconds
        searchBtn = searchForm.find("[type='submit']");

    searchInput.keyup(function (event) {
        // Key Release
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performsearch, typingInterval)

    });
    searchInput.keydown( function (event) {
        clearTimeout(typingTimer)
    });
    function displaySearching(){
        searchBtn.addClass('disable')
        searchBtn.html("<i class='fa fa-span fa-spinner'></i> Searching...")
    }
    function performsearch(){
        displaySearching()
        var query = searchInput.val()
        setTimeout(function() {
            window.location.href="/search?q=" + query

        }, 1000)
    };

/* ======================= Cart =============*/
    var productForm = $('.product_form_ajax');
    productForm.submit(function (e) {
        e.preventDefault()
        $this = $(this)

        var actionEndPoint = $this.attr('action'), // API end Point
            actionEndPoint = $this.attr('data-endpoint'),
            httpMethod = $this.attr('method'),
            formData = $this.serialize();

        $.ajax({
            url: actionEndPoint,
            method: httpMethod,
            data: formData,
            success: function(data){
                // console.log('Success')
                // console.log(data)
                var submitSpan = $this.find('.submit-span');
                if (data.added) {
                    submitSpan.html('<button type="submit" class="btn btn-danger">Remove From Cart</button>')
                } else {
                    submitSpan.html('<button type="submit" class="btn btn-danger">Cart Now</button>')
                }
                var navbarItemCount = $('.cart_item_count');
                navbarItemCount.text(data.cartItemCount);

                var currentPath = window.location.href
                if (currentPath.indexOf('cart') != -1) { // ('cart') is url cart address
                    refreshCart()
                }
            },
            error: function(errorData){
                console.log('Error')
                alert(errorData)
            }

        })

    });

    function refreshCart() {
        var cartTable = $('.cart-table'),
            cartBody = cartTable.find('.cart-body');
        var productRows = cartBody.find('.cart-products');
            // cartBody.html('Chnaged');
        var currentUrl = window.location.href;
        var refreshCartUrl = "api/";
        var refreshCartMethod = "GET";
        var data = {};

        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function(data) {
                console.log('success')
                console.log(data)
                if (data.products.length > 0 ) {

                    var hiddenForm = $('.cart-remove-hidden-form');

                    var i = data.products.length;
                    $.each(data.products, function(index, value) {
                        productRows.html(" ")
                        var newCartItemRemoveform = hiddenForm.clone();
                        newCartItemRemoveform.find('.cart_remove_id').val(value.id)
                        cartBody.prepend('<tr><td class="colspan">' + i + '</td><td><a href="' + value.url + '">' + value.name + '</a></td><td>' + value.price +  '</td><td>' + newCartItemRemoveform.html() + '</td></tr>')
                        i --
                    });
                    cartBody.find('.cart-sub-total').text(data.sub_total)
                    cartBody.find('.cart-total').text(data.total)
                    console.log("products: ")
                    console.log(data.products)
                    console.log("products length: " + data.products.length)
                } else {
                    window.location.href = currentUrl
                    console.log('else call')
                }
            },
            error: function(errorData) {
                console.log("Refresh Cart Error")
                console.log(errorData)
            }
        });

    };

});