import { createBrowserRouter } from "react-router-dom";

// Import the pages
import ProfilePage from "./pages/ProfilePage";
import StatsMainPage from "./pages/StatsMainPage";

// Import the layouts
import PageLayout from "./components/PageLayout";
import CreateUserPage from "./pages/CreateUserPage/CreateUserPage";
import CreateTeacherPage from "./pages/CreateTeacherPage/CreateTeacherPage";
import UpdateUserPage from './pages/UpdateUserPage/UpdateUserPage'

export const router = createBrowserRouter([
  {
    element: <PageLayout />,
    children: [
      {
        element: <ProfilePage />,
        path: "/profile",
      },
      {
        element: <StatsMainPage />,
        path: "/",
      },
      {
        element: <CreateUserPage />,
        path: "/users",
      },
      {
        element: <UpdateUserPage />,
        path: "/users/:userId",
      },
      {
        element: <CreateTeacherPage />,
        path: "/teachers",
      },
    ],
  },
]);
