const urlInput = document.getElementById("url-input-field");
const result = document.getElementById("result");
const copy = document.getElementById("copied");
const copyBtn = document.getElementById("copy");
const submitBtn = document.getElementById("submit-btn");
const serverURL = "http://localhost:8080/api/get_url";

async function postUserData(url, data) {
    try {
        const response = await fetch(url, {
            method:"POST",
            headers: {
                "Content-Type":"application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json()
        if (!response.ok) {
            throw new Error(
                `Status ${response.status}, ${result.message}`
            )
        };
        return result.shorturl

    } catch(error) {
        console.error("Signup failed:", error.message);
    }
}

submitBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const data = {
        url: urlInput.value
    };

    const shortURL = Promise.resolve(postUserData(serverURL, data));
    shortURL.then(value => result.textContent = value);  
})

copyBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const text = result.innerText;
    navigator.clipboard.writeText(text);
    
    alert("Copied!");
});
