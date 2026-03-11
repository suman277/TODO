import "./CreateTodo.css";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
export const CreateTodo = ({ modal, onCreate, todo }) => {
    const token = localStorage.getItem("token");
    const [formData, setFormData] = useState({
        todo: "",
        description: "",
        is_completed: false,
    });

    useEffect(() => {
        if (todo) {
            setFormData({
                todo: todo.todo,
                description: todo.description,
                is_completed: todo.is_completed,
            })
        }
    }, [todo])

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === "checkbox" ? checked : value
        }));
    }
    const navigate = useNavigate();

    const createTodo = () => {
        fetch("http://localhost:8000/todo/todos", {
            method: "PUT", // creating a todo → POST
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(formData), // ✅ PAYLOAD
        })
            .then(res => {
                if (!res.ok) {
                    throw new Error("Failed to create todo");
                }
                navigate("/todos")
            })
            .then(data => {
                console.log("Created:", data);
                modal()
                onCreate()
                navigate("/todo");
            })
            .catch(err => {
                console.error(err);
            });
    }

    const updateData = (id) => {
        const payload = {...formData, id:id,}
        fetch(`http://localhost:8000/todo/todos/`, {
            method: "PUT", // creating a todo → POST
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(payload),
        })
            .then(res => {
                if (!res.ok) {
                    throw new Error("Failed to create todo");
                }
                return res.json();
            })
            .then(data => {
                console.log("Created:", data);
                modal()
                onCreate()
                navigate("/todo");
            })
            .catch(err => {
                console.error(err);
            });
    }


const handleSubmit = (e) => {
    e.preventDefault(); // VERY IMPORTANT
    if (todo) {
        updateData(todo.id);
    } else {
        createTodo();
    }
};

return (
    <>
        <div className="todo-modal">
            <div className="create-todo"><h1>Todo</h1></div>
            <form className="todo-form">
                <label className="input-label">Username</label>
                <input
                    type="text"
                    name="todo"
                    className="todo-input"
                    placeholder="Enter todo title"
                    value={formData.todo}
                    onChange={handleChange}
                />
                <label className="input-label">Description</label>
                <input
                    type="text"
                    className="todo-input"
                    name="description"
                    placeholder="Enter todo Description"
                    value={formData.description}
                    onChange={handleChange}
                />
                <label className="input-label">Is Completed?</label>
                <div className="checkbox-wrapper">
                    <input type="checkbox" id="completed" name="is_completed" checked={formData.is_completed} onChange={handleChange} className="checkbox-item"></input>
                </div>
            </form>
            <div className="submit-wrapper">
                <button type="submit" className="todo-submit-button" onClick={handleSubmit}>
                    {todo ? "Update" : "Create"}
                </button>
                <button type="clear" className="todo-submit-button" onClick={modal}>
                    Cancel
                </button>
            </div>
        </div>
    </>
)
}

export default CreateTodo;

