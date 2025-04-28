import { createBrowserRouter } from "react-router-dom";

// Import the pages
import ProfilePage from "./pages/ProfilePage";
import StatsMainPage from "./pages/StatsMainPage";

// Import the layouts
import PageLayout from "./components/PageLayout";

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
    ],
  },
]);
