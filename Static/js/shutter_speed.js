$(document).ready(function() {
    $(".shutter-speed-title").click(function(e) {
        e.preventDefault();
        console.log("clicked");
        
        let img_index = parseInt($(this).data("img"), 10);
        let source = "/static/" + data.images[img_index];
        let alternate = data.alt[img_index];
        $("#sample-img").attr("src", source);
        $("#sample-img").attr("alt", alternate);
        $("#sample-img").show();
        $(".shutter-speed-title").removeClass("active");
        $(this).addClass("active");
    })
})