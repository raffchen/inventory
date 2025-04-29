import { Authenticated, Refine } from "@refinedev/core";
import { DevtoolsPanel, DevtoolsProvider } from "@refinedev/devtools";
import { RefineKbar, RefineKbarProvider } from "@refinedev/kbar";

import {
  ErrorComponent,
  ThemedLayoutV2,
  ThemedSiderV2,
  ThemedTitleV2,
  useNotificationProvider,
} from "@refinedev/antd";
import "@refinedev/antd/dist/reset.css";

import routerBindings, {
  CatchAllNavigate,
  DocumentTitleHandler,
  NavigateToResource,
  UnsavedChangesNotifier,
} from "@refinedev/react-router";
import { dataProvider } from "./providers/data-provider";
import dataProviderSimpleRest from "@refinedev/simple-rest";
import { ConfigProvider, App as AntdApp } from "antd";
import { BrowserRouter, Outlet, Route, Routes } from "react-router";
import { authProvider } from "./providers/authProvider";
import { Header } from "./components/header";
import { ColorModeContextProvider } from "./contexts/color-mode";
import { ForgotPassword } from "./pages/forgotPassword";
import { Login } from "./pages/login";
import { Register } from "./pages/register";
import { LensCreate, LensEdit, LensShow, LensList } from "./pages/lenses";

function App() {
  return (
    <BrowserRouter>
      <RefineKbarProvider>
        <ColorModeContextProvider>
          <ConfigProvider>
            <AntdApp>
              <DevtoolsProvider>
                <Refine
                  dataProvider={{
                    default: dataProvider(import.meta.env.VITE_API_URL),
                    fake_rest: dataProviderSimpleRest(
                      "https://api.fake-rest.refine.dev"
                    ),
                  }}
                  notificationProvider={useNotificationProvider}
                  routerProvider={routerBindings}
                  authProvider={authProvider}
                  resources={[
                    {
                      name: "lenses",
                      list: "/lenses",
                      show: "/lenses/:id",
                      edit: "/lenses/:id/edit",
                      create: "/lenses/create",
                      meta: { label: "Lenses" },
                    },
                  ]}
                  options={{
                    syncWithLocation: true,
                    warnWhenUnsavedChanges: true,
                    useNewQueryKeys: true,
                    projectId: "y71nmL-IAMfa9-lZZuF8",
                  }}
                >
                  <Routes>
                    <Route
                      element={
                        <Authenticated
                          key="authenticated-inner"
                          fallback={<CatchAllNavigate to="/login" />}
                        >
                          <ThemedLayoutV2
                            Header={Header}
                            Sider={(props) => <ThemedSiderV2 {...props} fixed />}
                            Title={(props) => (
                              <ThemedTitleV2 {...props} text="Inventory" />
                            )}
                          >
                            <Outlet />
                          </ThemedLayoutV2>
                        </Authenticated>
                      }
                    >
                      <Route index element={<NavigateToResource resource="lenses" />} />
                      <Route path="/lenses">
                        <Route index element={<LensList />} />
                        <Route path=":id" element={<LensShow />} />
                        <Route path=":id/edit" element={<LensEdit />} />
                        <Route path="create" element={<LensCreate />} />
                      </Route>
                    </Route>
                    <Route
                      element={
                        <Authenticated key="auth-pages" fallback={<Outlet />}>
                          <NavigateToResource resource="lenses" />
                        </Authenticated>
                      }
                    >
                      <Route path="/login" element={<Login />} />
                      <Route path="/register" element={<Register />} />
                      <Route path="/forgot-password" element={<ForgotPassword />} />
                    </Route>
                  </Routes>
                  <RefineKbar />
                  <UnsavedChangesNotifier />
                  <DocumentTitleHandler />
                </Refine>
                <DevtoolsPanel />
              </DevtoolsProvider>
            </AntdApp>
          </ConfigProvider>
        </ColorModeContextProvider>
      </RefineKbarProvider>
    </BrowserRouter>
  );
}

export default App;
