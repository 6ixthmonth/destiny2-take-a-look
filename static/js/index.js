function conn() {
    // var apiKey = "";

    // $.ajax({
    //     url: "https://www.bungie.net/platform/Destiny/Manifest/InventoryItem/1274330687/",
    //     headers: {
    //         "X-API-Key": apiKey
    //     }
    // }).done(function (json) {
    //     console.log(json.Response.data.inventoryItem.itemName); //Gjallarhorn
    // });

    $.ajax({
        url: "apitest/conntest/",
        type: "get",
        // data: {

        // },
        headers: {
            'X-CSRFTOKEN': '{{ csrf_token }}'
        },
        success: function(res) {
            console.log(res);
        },
        error: function(e) {
            console.log(e);
        }
    });
}