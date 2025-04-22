import { Toolbar, SaveButton } from "react-admin";
import { DeleteWithConfirm } from "./button";

export const CustomEditToolbar = () => (
  <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
    <SaveButton />
    <DeleteWithConfirm />
  </Toolbar>
);
