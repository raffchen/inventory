import { DeleteButton, Toolbar, SaveButton } from "react-admin";

export const CustomEditToolbar = () => (
  <Toolbar sx={{ display: "flex", justifyContent: "space-between" }}>
    <SaveButton />
    <DeleteButton mutationMode="pessimistic" />
  </Toolbar>
);
