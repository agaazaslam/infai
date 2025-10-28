import { createBrowserRouter } from "react-router";
import About from "../pages/About";
import News from "../pages/News";
import Chat from "../pages/Chat";
import NotFound from "../pages/NotFound";



const router = createBrowserRouter([
  {
    path: "/",
    children: [
      { index: true, element: <News /> },
      { path: "chat", element: <Chat /> },
      { path: "news", element: <News /> },
      { path: "about", element: <About /> },
      { path: "*", element: <NotFound /> },
    ],
  },
]);

export default router
