class ApiRequest {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    async post(endpoint, data) {
        const response = await fetch(`${this.baseUrl}/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    async get(endpoint) {
        const response = await fetch(`${this.baseUrl}/${endpoint}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    }

    get_user_endpoint(endpoint, username){
        if (username === undefined || username.trim() === "") {
            return endpoint.replace("/{username}", "");
        }
        return endpoint.replace("{username}", username);
    }

}

export { ApiRequest };