function getAuth() {
    alert("{% url 'd2api:get_auth' %}");
    $.ajax({
        url: "{% url 'd2api:get_auth' %}"
    }).done(function (res) {
        location.href = res['auth_response_url']
    }).fail(function (e) {
        console.log(e);
    });
}

function req() {
    // alert(location.search);

    $.ajax({
        url: "/d2api/req/",
        data: JSON.stringify({
            'auth_res': location.search
        })
    }).done(function (res) {
        console.log("success");
        console.log(res);
    }).fail(function (e) {
        console.log("error");
        console.log(e);
    });
}