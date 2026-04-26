import { createBrowserRouter } from "react-router";
import { AppShell } from "./components/chrome/AppShell";
import { Home } from "./pages/Home";
import { Search } from "./pages/Search";
import { Repository } from "./pages/Repository";
import { Pipeline } from "./pages/Pipeline";
import { SermonDetail } from "./pages/SermonDetail";

export const router = createBrowserRouter([
  {
    path: "/",
    Component: AppShell,
    children: [
      { index: true, Component: Home },
      { path: "search", Component: Search },
      { path: "repository", Component: Repository },
      { path: "pipeline", Component: Pipeline },
      { path: "video/:id", Component: SermonDetail },
    ],
  },
]);
