import { createBrowserRouter, Navigate } from "react-router-dom";
import Login from "../Login/Login";
import App from "../App";
import ActivityLogs from "../activity-logs/ActivityLogs";
import Signup from "../Login/Signup"
import Agent from "../agentic-ai/Agent";
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
    path: "/login",
    element: <Login />
  },
  {
    path: "/todo",
    element: (
      <IsProtected>
        <App />
      </IsProtected>
    ),
  },
  {
    path: "/logs",
    element: (
      <IsProtected>
        <ActivityLogs />
      </IsProtected>
    )
  },
  {
    path: "/signup",
    element: <Signup />
  },
  {
    path: "/agent",
    element: <Agent/>
  },
  {
    path: "*",
    element: <div>404 - Page not found</div>   // or your custom NotFound component
  }
]);



// import { createBrowserRouter, Navigate } from "react-router-dom";
// import App from "../App";
// import Login from "../Login/Login";
// import ActivityLogs from "../activity-logs/ActivityLogs";

// export const router = createBrowserRouter([
//   { path: "/", element: <Navigate to="/login" replace /> },

//   { path: "/login", element: <Login /> },

//   { path: "/todo", element: <IsProtected><App /></IsProtected> },

//   { path: "/logs", element: <ActivityLogs /> },

//   { path: "*", element: <div>404 - Page not found</div> }
// ]);
