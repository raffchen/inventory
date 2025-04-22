import { Admin, Resource } from "react-admin";
import simpleRestProvider from "ra-data-simple-rest";
import { LensEdit, LensList, LensShow } from "./lenses";

export const App = () => (
  <Admin
    dataProvider={simpleRestProvider("http://localhost:8000/api/inventory")}
  >
    <Resource name="lenses" list={LensList} show={LensShow} edit={LensEdit} />
  </Admin>
);
