function getAuth() {
    $.ajax({
        url: "{% url 'd2api:get_auth' %}"
    }).done(function (res) {
        location.href = res['auth_response_url']
    }).fail(function (e) {
        console.log(e);
    });
}

function requestData() {
    $.ajax({
        url: "{% url 'd2api:req_data' %}",
        type: "post",
        data: JSON.stringify({
            'auth_res': location.search
        }),
        headers: {
            'X-CSRFTOKEN': "{{ csrf_token }}"
        }
    }).done(function (res) {
        console.log("success");
        console.log(res);
    }).fail(function (e) {
        console.log("error");
        console.log(e);
    });
}