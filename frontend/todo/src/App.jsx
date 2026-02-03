import { useEffect, useState } from 'react'
import './App.css'
import { TodoList } from './TodoList'
import CreateTodo from "./create-todo/CreateTodo"
import { useGetAPI } from "../apiClient";
import { useNavigate } from 'react-router-dom';


function App() {
  const [todos, setTodos] = useState([]);
  const [openModal, setOpenModal] = useState(false)
  const [selectedTodo, setSelectedTodo] = useState(null)
  const [search, setSearch] = useState("")
  const closeModal = () => {
    setOpenModal(false);
    setSelectedTodo(null);
  };

  const handleCreate = () => {
    setSelectedTodo(null);
    setOpenModal(true);
  }

  const handleEdit = (id) => {
    console.log("kuch hua ki nhi");
    fetchTodobyId(id)
  }

  const handleSearch = (e) => {
    setSearch(e.target.value);
  }
  const navigator = useNavigate()
  const token = localStorage.getItem("token");
  const fetchTodos = () => {
    const url = new URL("http://localhost:8000/todo/todos");

    if (search && search.trim()) {
      url.searchParams.append("search", search.trim());
    }

    fetch(url.toString(), {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then(res => {
        if (res.status == 401) {
          navigator("/login")
          throw new Error("AUTHORIZATION FAILED")
        }
        if (!res.ok) throw new Error("Failed");
        console.log(res);
        return res.json();
      })
      .then(data => {
        setTodos(Array.isArray(data) ? data : data.data ?? []);
      })
      .catch(() => setTodos([]));
  };

  const handleDelete = (id) => {
    console.log("Delete", id)
    fetch("http://localhost:8000/todo/todos/" + id, {
      method: "DELETE",
      headers: {
        "Content-type": "application/json",
        Authorization: `Bearer ${token}`,
      }
    })
      .then(res => {
        if (res.status === 401) {
          navigator("/login");
        }
        if (!res.ok) {
          throw new Error("An Error Occured")
        }
      })
      .then(() => {
        fetchTodos()
      })
  }

  const fetchTodobyId = (id) => {
    fetch("http://localhost:8000/todo/todos/" + id, {
      method: "GET",
      headers: {
        "content-type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then(res => {
        if (res.status === 401) {
          navigator("/login")
        }
        if (!res.ok) {
          throw new Error("An error Occured");
        }
        return res.json();
      })
      .then(data => {
        setSelectedTodo(data);
        setOpenModal(true)
      })
      .catch(() => {
        console.error("An error occured")
      })
  }

  useEffect(() => {
    fetchTodos()
  }, [search])

  return (
    <>
      <div className='todo-main'>
        <div className='todo-header'>
          <div className='todo'>Todo</div>
        </div>
        <div className='todo-logic'>
          <input className='todo-input' placeholder='Enter Todo' onChange={handleSearch} />
          {todos.map((todo) => (
            <TodoList key={todo.id} todo={todo} handleDelete={handleDelete} handleEdit={handleEdit} handleModal={handleEdit} />
          ))}
          <div>
          </div>
        </div>
        {openModal && <CreateTodo modal={closeModal} onCreate={fetchTodos} todo={selectedTodo} />}
        <div className='add-todo'>
          <button className='text' onClick={handleCreate}>+</button>
        </div>
      </div>
    </>
  )
}

export default App;


