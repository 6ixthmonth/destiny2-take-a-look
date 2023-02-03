function conn() {
    $.ajax({
        url: "apitest/conntest/",
        headers: {
            "X-CSRFTOKEN": "{{ csrf_token }}"
        },
    }).done(function (res) {
        console.log("success");
        console.log(res);
    }).fail(function (res) {
        console.log("error");
        console.log(e);
    });
}