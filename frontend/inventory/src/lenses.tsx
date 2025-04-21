import { Datagrid, DateField, List, NumberField, TextField } from "react-admin";

export const LensList = () => (
  <List>
    <Datagrid>
      <TextField source="id" />
      <TextField source="lens_type" />
      <NumberField source="sphere" />
      <NumberField source="cylinder" />
      <NumberField source="unit_price" />
      <NumberField source="quantity" />
      <NumberField source="storage_limit" />
      <TextField source="comment" />
      <DateField source="created_at" />
      <DateField source="updated_at" />
    </Datagrid>
  </List>
);
