import { createBrowserRouter, Navigate } from "react-router-dom";
import Login from "../Login/Login";
import App from "../App";

const IsProtected = ({ children }) => {
  if (!localStorage.getItem("token")) {
    return <Navigate to="/" replace />
  }
  return children;
}
export const router = createBrowserRouter([
  {
    path: "/", element: <Navigate to="/login" replace />
  },
  {
    path: "/login",           // ← add this
    element: <Login />
  },
  {
    path: "/todo",
    element: (
      <IsProtected>
        <App />
      </IsProtected>
    )
  },
  // Optional: catch-all for 404
  {
    path: "*",
    element: <div>404 - Page not found</div>   // or your custom NotFound component
  }
]);