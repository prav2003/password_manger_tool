document.addEventListener("DOMContentLoaded", function () {
    const passwordForm = document.getElementById("password-form");
    const getPasswordButton = document.getElementById("get-password");
    const resultDiv = document.getElementById("result");
    const getPasswordResultDiv = document.getElementById("get-password-result");

    passwordForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const account = document.getElementById("account").value;
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const action = document.getElementById("action").value;

        const data = {
            account: account,
            username: username,
            password: password,
            action: action
        };

        fetch("http://127.0.0.1:5000/add-password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.textContent = data.message;
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });

    getPasswordButton.addEventListener("click", function (event) {
        console.log("get password");
        const account = document.getElementById("account").value;

        fetch(`http://127.0.0.1:5000/get-password?account=${account}`)
            .then(response => response.json())
            .then(data => {
                getPasswordResultDiv.textContent = data.message;
            })
            .catch(error => {
                console.log("account", account);
                console.error("Error:", error);
            });
    });
});