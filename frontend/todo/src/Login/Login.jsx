import "./Login.css"
import { useState } from "react";
import {useNavigate} from "react-router-dom";


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
    const handleSubmit = (e) => {
        e.preventDefault();
            fetch("http://localhost:8000/user/login", {
        method: "POST", // make sure backend really expects PUT
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
    })
        .then(res => {
            if (!res.ok) {
                throw new Error("Login failed");
            }
            return res.json();
        })
        .then(data => {
            // 🔥 store response here
            localStorage.setItem("loginResponse", JSON.stringify(data));
            navigate("/todo")

            // example: store token separately (best practice)
            if (data.access_token) {
                localStorage.setItem("token", data.access_token);
            }

            console.log("Login success:", data);
        })
        .catch(err => {
            console.log("Error occurred while logging in:", err);
        });
    }

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