import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Login from './Login/Login.jsx'
import CreateTodo from './create-todo/CreateTodo.jsx'
import { RouterProvider } from "react-router-dom";;
import { router } from './routers/Routers.jsx'
import ActivityList from "./activity-logs/ActivityList.jsx"
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
    {/* <ActivityList/> */}
  </StrictMode>,
)
