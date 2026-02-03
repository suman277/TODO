import "./Login.css"
import { useState } from "react";
import { useNavigate } from "react-router-dom";


export const Login = () => {
    const [formData, setFormData] = useState({
        username: "",
        password: "",
    });


    const handleChange = (e) => {
        e.preventDefault();
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }))
    }
    const navigate = useNavigate();
    // const handleSubmit = (e) => {
    //     e.preventDefault();
    //         fetch("http://localhost:8000/user/login", {
    //     method: "POST", // make sure backend really expects PUT
    //     headers: {
    //         "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify(formData),
    // })
    //     .then(res => {
    //         if (!res.ok) {
    //             throw new Error("Login failed");
    //         }
    //         return res.json();
    //     })
    //     .then(data => {
    //         // 🔥 store response here
    //         localStorage.setItem("loginResponse", JSON.stringify(data));

    //         // example: store token separately (best practice)
    //         if (data.access_token) {
    //             localStorage.setItem("token", data.access_token);
    //         }

    //         console.log("Login success:", data);
    //     })
    //     .catch(err => {
    //         console.log("Error occurred while logging in:", err);
    //     });
    // }
    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            // 1️⃣ Login API
            const loginRes = await fetch("http://localhost:8000/user/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (!loginRes.ok) {
                throw new Error("Login failed");
            }

            const loginData = await loginRes.json();

            // 2️⃣ Store token immediately
            if (!loginData.access_token) {
                throw new Error("Token missing in login response");
            }

            localStorage.setItem("token", loginData.access_token);

            // 3️⃣ Call INFO API using token
            const infoRes = await fetch("http://localhost:8000/user/info", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${loginData.access_token}`,
                    "Content-Type": "application/json",
                },
            });

            if (!infoRes.ok) {
                throw new Error("Failed to fetch user info");
            }

            const userInfo = await infoRes.json();

            // 4️⃣ Store user id (only what you need)
            localStorage.setItem("userId", userInfo.user_id);

            // (optional) store minimal user object
            localStorage.setItem("user", JSON.stringify({
                id: userInfo.id,
                name: userInfo.name,
                email: userInfo.email,
            }));

            console.log("Login + user info success", userInfo);

            // 5️⃣ Navigate only after everything succeeds
            navigate("/todo");

        } catch (err) {
            console.error("Login flow failed:", err.message);
        }
    };

    return (
        <>
            <div className="login-container">
                <div className="modal">
                    <h2 className="login-header">Login</h2>
                    <form className="login-form">
                        <div className="username">
                            <label className="input-label">Username</label>
                            <input type="text" placeholder="Username" className="login-input" name="username" onChange={handleChange} value={formData.username} required />
                        </div>
                        <div className="password">
                            <label className="input-label">Password</label>
                            <input type="password" placeholder="Password" className="login-input" name="password" onChange={handleChange} value={formData.password} required />
                        </div>
                        <div className="buttons">
                            <button type="submit" className="login-button" onClick={handleSubmit}>Login</button>
                            <button type="submit" className="signup-button">Sign Up</button>
                        </div>
                    </form>
                </div>
            </div>
        </>
    )

}

export default Login;