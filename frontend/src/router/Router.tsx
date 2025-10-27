import { createBrowserRouter } from "react-router";
import About from "../pages/About";
import News from "../pages/News";
import Chat from "../pages/Chat";



const router = createBrowserRouter([
  {
    path: "/",
    children: [
      { index: true, element: <News /> },
      { path: "chat", element: <Chat /> },
      { path: "news", element: <News /> },
      { path: "about", element: <About /> },
    ],
  },
]);

export default router
