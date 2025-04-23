import { createBrowserRouter } from "react-router-dom";

// Import the pages

import ProfilePage from "./pages/ProfilePage";

export const router = createBrowserRouter([
  {
    element: <ProfilePage />,
    path: "/profile",
  },
]);
