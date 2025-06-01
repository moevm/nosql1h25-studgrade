import { createBrowserRouter } from "react-router-dom";

// Import the pages
import ProfilePage from "./pages/ProfilePage";
import StatsMainPage from "./pages/StatsMainPage";

// Import the layouts
import PageLayout from "./components/PageLayout";
import CreateUserPage from "./pages/CreateUserPage/CreateUserPage";

import UpdateUserPage from './pages/UpdateUserPage/UpdateUserPage'

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
        path: "/users",
      },
      {
        element: <UpdateUserPage />,
        path: "/users/:userId/update",
      },
    ],
  },
]);
