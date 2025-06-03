import { createBrowserRouter } from "react-router-dom";

// Import the pages
import ProfilePage from "./pages/ProfilePage";
import StatsMainPage from "./pages/StatsMainPage";

// Import the layouts
import PageLayout from "./components/PageLayout";
import CreateUserPage from "./pages/CreateUserPage/CreateUserPage";
import CreateAdminPage from "./pages/CreateAdminPage/CreateAdminPage";
import CreateTeacherPage from "./pages/CreateTeacherPage/CreateTeacherPage";
import UpdateUserPage from './pages/UpdateUserPage/UpdateUserPage'
import UserPage from "./pages/UserPage/UserPage";

export const router = createBrowserRouter([
  {
    element: <PageLayout />,
    children: [
      {
        element: <ProfilePage role='user' />,
        path: "/users/:userId",
      },
      {
        element: <StatsMainPage />,
        path: "/",
      },
      {
        element: <CreateUserPage />,
        path: "/users/create",
      },
      {
        element: <CreateTeacherPage />,
        path: "/teachers/create",
      },
      {
        element: <CreateAdminPage />,
        path: "/admins/create",
      },
      {
        element: <UpdateUserPage />,
        path: "/users/:userId/update",
      },
      {
        element: <UserPage />,
        path: "/users",
      },
    ],
  },
]);
