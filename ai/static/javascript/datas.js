$.getJSON("/totaltweets", function (data) {
    reading(data)
});

function reading(data) {
    document.getElementById("total-tweets").innerHTML = Number(data[0]["totaltweets"]).toLocaleString();
    document.getElementById("total-users").innerHTML = Number([data[1]["totalusers"]]).toLocaleString();
    document.getElementById("verifiedusers").innerHTML = Number([data[2]["verified"]]).toLocaleString();
}